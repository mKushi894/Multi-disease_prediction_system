"""
Gemini AI assistant helpers (google-genai SDK). Returns None when unavailable.
"""
import streamlit as st

from src.utils.settings import get_secret

SYSTEM_PROMPT = (
    "You are a helpful healthcare information assistant for a multi-disease "
    "prediction app. Provide general, educational health information. "
    "Never diagnose or replace a clinician. Always include a short medical "
    "disclaimer. Keep answers concise and clear."
)

MODEL_NAME = "gemini-3.5-flash"


def gemini_status():
    """Return 'ok', 'missing_key', or 'missing_sdk' for a precise UI hint."""
    if not get_secret("GEMINI_API_KEY"):
        return "missing_key"
    try:
        from google import genai  # noqa: F401
    except Exception:
        return "missing_sdk"
    return "ok"


def get_gemini_model():
    key = get_secret("GEMINI_API_KEY")
    if not key:
        return None
    try:
        from google import genai

        return genai.Client(api_key=key)
    except Exception:
        return None


def ask(client, history, user_msg, context=None):
    """Send a message and return assistant text. history: list of {role, content}."""
    if client is None:
        return "AI assistant is not configured (missing GEMINI_API_KEY)."
    try:
        from google.genai import types

        gem_history = [
            types.Content(
                role="model" if m.get("role") == "assistant" else m.get("role", "user"),
                parts=[types.Part(text=m.get("content", ""))],
            )
            for m in history
        ]
        chat = client.chats.create(
            model=MODEL_NAME,
            history=gem_history,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        msg = user_msg
        if context:
            msg = f"{user_msg}\n\nContext (do not echo verbatim): {context}"
        last_err = None
        for _ in range(2):
            try:
                response = chat.send_message(msg)
                return getattr(response, "text", str(response))
            except Exception as e:
                last_err = e
                if "503" in str(e) or "UNAVAILABLE" in str(e).upper():
                    import time
                    time.sleep(1.2)
                    continue
                break
        if "RESOURCE_EXHAUSTED" in str(last_err) or "quota" in str(last_err).lower():
            return "The AI assistant has reached its daily usage limit. Please try again later."
        return f"Assistant error: {last_err}"
    except Exception as e:
        return f"Assistant error: {e}"
