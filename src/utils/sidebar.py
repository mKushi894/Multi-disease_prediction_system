"""
Shared sidebar: brand, account chip and navigation only. Language, display
settings and the AI assistant live in the top header bar.
"""
import html

import streamlit as st

from src.auth.auth_ui import current_user, logout
from src.auth.storage import display_name
from src.i18n import t


def _nav():
    st.markdown(f'<div class="nav-group">{t("screening")}</div>', unsafe_allow_html=True)
    st.page_link("app.py", label=t("home"), icon="🏠")
    st.page_link("pages/1_Heart_Disease.py", label=t("heart"), icon="❤️")
    st.page_link("pages/2_Kidney_Disease.py", label=t("kidney"), icon="🫘")
    st.page_link("pages/3_Liver_Disease.py", label=t("liver"), icon="🫀")
    st.page_link("pages/4_Lung_Disease.py", label=t("lung"), icon="🫁")
    st.page_link("pages/5_Breast_Cancer.py", label=t("breast"), icon="🎗️")
    st.markdown(f'<div class="nav-group">{t("insights")}</div>', unsafe_allow_html=True)
    st.page_link("pages/6_History.py", label=t("history"), icon="📜")
    st.page_link("pages/7_Health_Education.py", label=t("education"), icon="📚")
    st.page_link("pages/8_About_Model.py", label=t("about"), icon="🧠")
    st.markdown(f'<div class="nav-group">{t("support")}</div>', unsafe_allow_html=True)
    st.page_link("pages/9_Feedback.py", label=t("feedback"), icon="💬")


def render_sidebar():
    user = current_user()

    with st.sidebar:
        st.markdown(
            """
            <div class="brand">
                <div class="brand-mark">🩺</div>
                <div>
                    <div class="brand-name">Multi-Disease</div>
                    <div class="brand-sub">Prediction System</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if user is not None:
            name = display_name(user)
            initial = html.escape((name or "U").strip()[0].upper())
            st.markdown(
                f"""
                <div class="user-chip">
                    <div class="avatar">{initial}</div>
                    <div class="user-meta">
                        <div class="user-name">{html.escape(name)}</div>
                        <div class="user-state">Signed in</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Log out", width="stretch"):
                logout()

        _nav()
        st.caption("Academic prototype · Group 17")
