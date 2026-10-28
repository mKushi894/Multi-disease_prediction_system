"""
Docsy Clinical AI Copilot — Native Streamlit Implementation.
Clean, lightweight, zero-boilerplate medical assistant dialog.
Eliminates background HTTP servers, custom JS, DOM hacks, and regex parsers.
"""
import streamlit as st

from src.chatbot.gemini import ask, get_gemini_model


def _get_active_context_summary() -> str | None:
    last_pred = st.session_state.get("last_prediction")
    if not last_pred:
        return None
    disease = str(last_pred.get("disease", "")).replace("_", " ").title()
    res = last_pred.get("result", {}) or {}
    label = res.get("result_label", "")
    conf = res.get("confidence", "")
    inputs = res.get("user_inputs") or res.get("input_features", {})
    return (
        f"Active screening: {disease}. "
        f"Result: {label} ({conf}% confidence). "
        f"Patient biomarkers: {inputs}"
    )


def handle_send_message(prompt: str):
    """Processes a user prompt and queries the Gemini clinical assistant."""
    history = st.session_state.setdefault("docsy_chat_history", [])
    history.append({"role": "user", "content": prompt})

    context = _get_active_context_summary()
    model = get_gemini_model()
    if not model:
        reply = (
            "⚠️ Gemini API key is missing or unconfigured. "
            "Please check `GEMINI_API_KEY` in `.streamlit/secrets.toml`."
        )
    else:
        with st.spinner("Docsy is reviewing clinical knowledge..."):
            reply = ask(model, history[:-1], prompt, context=context)

    history.append({"role": "assistant", "content": reply})


@st.dialog("Docsy — Clinical AI Copilot", width="large")
def show_docsy_dialog():
    """Native Streamlit dialog for Docsy AI copilot."""
    last_pred = st.session_state.get("last_prediction")
    history = st.session_state.setdefault("docsy_chat_history", [])

    # Header row: Context banner & Reset button
    top_left, top_right = st.columns([5, 1])
    with top_left:
        if last_pred:
            disease = str(last_pred.get("disease", "")).replace("_", " ").title()
            res = last_pred.get("result", {}) or {}
            label = res.get("result_label", "")
            conf = res.get("confidence", "")
            st.info(f"📋 **Active Screening**: {disease} — {label} ({conf}%)", icon="🩺")
        else:
            st.caption("Ask questions about cardiovascular, renal, hepatic, or pulmonary screening, biomarkers, and guidelines.")
    with top_right:
        if st.button("＋ New", help="Start new conversation", use_container_width=True):
            st.session_state["docsy_chat_history"] = []
            st.rerun()

    # Empty State with Quick Clinical Prompts
    if not history:
        st.markdown("##### Quick Clinical Prompts")
        suggestions = [
            ("📊 Explain current screening", "Explain the active clinical screening result and key risk contributors."),
            ("🫀 Review cardiac biomarkers", "Review key cardiac biomarkers: Oldpeak ST depression, Thalassemia defect, and vessel fluoroscopy."),
            ("🩸 Blood pressure stages", "Explain the clinical difference between Prehypertension and Stage 1/2 Hypertension."),
            ("🫘 Renal filtration markers", "How do Serum Creatinine, Blood Urea, and Albumin indicate renal filtration capacity?"),
            ("🧪 Liver enzyme thresholds", "What do elevated SGOT (AST), SGPT (ALT), and Alkaline Phosphatase indicate clinically?"),
            ("🥗 Evidence-based prevention", "What are evidence-based lifestyle habits to lower cardiovascular and renal risk?"),
        ]
        sug_cols = st.columns(2)
        for i, (label, prompt_text) in enumerate(suggestions):
            with sug_cols[i % 2]:
                if st.button(label, key=f"docsy_sug_{i}", use_container_width=True):
                    handle_send_message(prompt_text)
                    st.rerun()

    # Message Thread (renders headers, bold, lists, code, and math natively)
    if history:
        chat_container = st.container(height=380)
        with chat_container:
            for msg in history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Ask Docsy... (e.g., 'What do elevated liver enzymes mean?')"):
        handle_send_message(prompt)
        st.rerun()


def render_copilot(page_key: str = "home", **kwargs):
    """
    Renders the Copilot trigger button in the top header bar.
    Clicking it opens the native Streamlit dialog.
    """
    last_pred = st.session_state.get("last_prediction")
    btn_type = "primary" if last_pred else "secondary"
    btn_label = "✨ Explain Result" if last_pred else "✨ Docsy AI"

    if st.button(btn_label, key=f"docsy_hdr_btn_{page_key}", type=btn_type, help="Open Docsy Clinical Copilot"):
        show_docsy_dialog()
