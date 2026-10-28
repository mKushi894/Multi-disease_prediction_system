"""
Feedback page.
"""
import streamlit as st
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.auth.auth_ui import require_login
from src.auth.storage import save_feedback
from src.utils.ui_components import inject_custom_css, page_header, render_disclaimer
from src.utils.sidebar import render_sidebar
from src.i18n import t
from src.utils.header import render_header

st.set_page_config(page_title="Feedback | MDPS", page_icon="💬", layout="wide")
inject_custom_css()
require_login()
render_sidebar()
render_header(page_key="feedback")

page_header("💬", t("page_feedback_title"), t("page_feedback_sub"))

with st.form("feedback_form"):
    rating = st.selectbox("How easy was the app?", ["Very easy", "Easy", "Neutral", "Difficult", "Very difficult"])
    comments = st.text_area("Suggestions or comments", placeholder="Optional")
    submitted = st.form_submit_button("Submit feedback", width="stretch")

if submitted:
    saved = save_feedback(rating, comments)
    if saved:
        st.success("Thank you! Your feedback was saved.")
    else:
        st.success("Thank you! Your feedback was recorded for this session.")

render_disclaimer()
