"""
Top header bar: language selector, display settings and the AI assistant copilot trigger.

Kept compact (single 44px row) so it doesn't eat vertical space. Controls
the clinical copilot slide-over drawer and user display preferences.
"""
import streamlit as st

from src.i18n import LANGUAGES, t
from src.utils.copilot import render_copilot


def _sync_language():
    label = st.session_state.get("ui_language_label", "English")
    if label not in LANGUAGES:
        label = "English"
    st.session_state["ui_language_label"] = label
    st.session_state["ui_language"] = LANGUAGES[label]


def render_header(page_key: str = "home"):
    _sync_language()

    left, right = st.columns([5, 3])
    with left:
        st.markdown('<div class="header-left-spacer"></div>', unsafe_allow_html=True)
    with right:
        c_copilot, c_lang, c_settings = st.columns([1.5, 1.3, 0.7])
        with c_copilot:
            render_copilot(page_key=page_key)
        with c_lang:
            current = st.session_state.get("ui_language_label", "English")
            wkey = "ui_language_select_" + page_key
            st.session_state.setdefault(wkey, current if current in LANGUAGES else "English")
            new_lang = st.selectbox(
                t("language"),
                list(LANGUAGES.keys()),
                key=wkey,
                label_visibility="collapsed",
                format_func=lambda x: "🌐 " + x,
            )
            if new_lang != current:
                st.session_state["ui_language_label"] = new_lang
                st.session_state["ui_language"] = LANGUAGES[new_lang]
                st.rerun()
        with c_settings:
            with st.popover("⚙️", help=t("settings")):
                theme_cur = st.session_state.get("ui_theme", "Light")
                wkey = "ui_theme_select_" + page_key
                st.session_state.setdefault(wkey, theme_cur)
                new_theme = st.selectbox(t("theme"), ["Light", "Dark"], key=wkey)
                if new_theme != theme_cur:
                    st.session_state["ui_theme"] = new_theme
                    st.rerun()
    st.markdown('<div class="header-rule"></div>', unsafe_allow_html=True)
