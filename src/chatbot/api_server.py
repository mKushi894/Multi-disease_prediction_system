"""
Lightweight background HTTP API server for Docsy Copilot.
Enables real-time, non-blocking asynchronous chat interactions
without triggering Streamlit page reruns or layout shifts.
"""
import http.server
import json
import logging
import socket
import threading
from typing import Any, Dict, Optional

from src.auth.storage import save_chat_message
from src.chatbot.gemini import ask, gemini_status, get_gemini_model

logger = logging.getLogger("docsy_api_server")

_ACTIVE_CONTEXT: Dict[str, Any] = {}
_SERVER_THREAD: Optional[threading.Thread] = None
_SERVER_INSTANCE: Optional[http.server.ThreadingHTTPServer] = None
_SERVER_PORT = 8503


def get_active_context() -> Dict[str, Any]:
    return dict(_ACTIVE_CONTEXT)


def set_active_context(disease: str, result: Dict[str, Any], inputs: Optional[Dict[str, Any]] = None):
    global _ACTIVE_CONTEXT
    res_label = result.get("result_label", "")
    conf = result.get("confidence", "")
    prob = result.get("probability_positive", "")
    _ACTIVE_CONTEXT = {
        "disease": disease,
        "result_label": res_label,
        "confidence": conf,
        "probability_positive": prob,
        "inputs": inputs or result.get("user_inputs") or result.get("input_features", {}),
        "summary": f"{disease.replace('_', ' ').title()} — {res_label} ({conf}%)",
    }


class DocsyApiHandler(http.server.BaseHTTPRequestHandler):
    def _send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors()
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/api/status"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "gemini": gemini_status()}).encode("utf-8"))
        elif self.path.startswith("/api/context"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors()
            self.end_headers()
            self.wfile.write(json.dumps({"context": _ACTIVE_CONTEXT}).encode("utf-8"))
        else:
            self.send_response(404)
            self._send_cors()
            self.end_headers()

    def do_POST(self):
        global _ACTIVE_CONTEXT
        length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(length) if length > 0 else b"{}"
        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception:
            payload = {}

        if self.path.startswith("/api/chat"):
            user_msg = payload.get("message", "").strip()
            history = payload.get("history", [])
            context = payload.get("context")

            if not context and _ACTIVE_CONTEXT:
                context = (
                    f"Active screening module: {_ACTIVE_CONTEXT.get('disease')}. "
                    f"Prediction: {_ACTIVE_CONTEXT.get('result_label')} with {_ACTIVE_CONTEXT.get('confidence')}% confidence. "
                    f"Patient inputs: {_ACTIVE_CONTEXT.get('inputs')}"
                )

            if not user_msg:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self._send_cors()
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Empty message"}).encode("utf-8"))
                return

            model = get_gemini_model()
            if not model:
                reply = (
                    "⚠️ Gemini API key is missing or invalid. Please check `GEMINI_API_KEY` "
                    "in `.streamlit/secrets.toml`."
                )
            else:
                try:
                    reply = ask(model, history, user_msg, context=context)
                    save_chat_message("user", user_msg)
                    save_chat_message("assistant", reply)
                except Exception as e:
                    reply = f"Clinical Copilot error: {e}"

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors()
            self.end_headers()
            self.wfile.write(json.dumps({"reply": reply}).encode("utf-8"))

        elif self.path.startswith("/api/context"):
            _ACTIVE_CONTEXT = payload.get("context", {})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "context": _ACTIVE_CONTEXT}).encode("utf-8"))
        else:
            self.send_response(404)
            self._send_cors()
            self.end_headers()

    def log_message(self, format, *args):
        # Silence default stderr logging to keep console clean
        pass


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def ensure_api_server_started(port: int = 8503) -> int:
    global _SERVER_THREAD, _SERVER_INSTANCE, _SERVER_PORT
    if _SERVER_INSTANCE is not None:
        return _SERVER_PORT

    target_port = port
    # Find free port if 8503 is occupied
    for p in range(target_port, target_port + 10):
        if not is_port_in_use(p):
            target_port = p
            break

    try:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", target_port), DocsyApiHandler)
        _SERVER_INSTANCE = server
        _SERVER_PORT = target_port
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        _SERVER_THREAD = t
    except Exception as e:
        logger.warning(f"Could not start Docsy API server: {e}")

    return _SERVER_PORT
