"""
Health education page — plain-language prevention guidance.
"""
import streamlit as st
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.auth.auth_ui import require_login
from src.utils.ui_components import inject_custom_css, page_header, render_disclaimer
from src.utils.sidebar import render_sidebar
from src.i18n import t
from src.utils.header import render_header

st.set_page_config(page_title="Health Education | MDPS", page_icon="📚", layout="wide")
inject_custom_css()
require_login()
render_sidebar()
render_header(page_key="education")

page_header("📚", t("page_education_title"), t("page_education_sub"))

with st.expander("❤️ Heart health", expanded=True):
    st.markdown(
        "- Keep blood pressure below 120/80 mmHg where possible.\n"
        "- Aim for 150 minutes of moderate activity per week.\n"
        "- Eat more vegetables, fruit, whole grains, and less salt and fried food.\n"
        "- Do not smoke; limit alcohol.\n"
        "- Seek care for chest pain, breathlessness, or fainting."
    )

with st.expander("🫀 Liver health"):
    st.markdown(
        "- Limit alcohol and avoid unnecessary medicines.\n"
        "- Maintain a healthy weight; fatty liver is common.\n"
        "- Get vaccinated for hepatitis B where recommended.\n"
        "- Seek care for yellow eyes, dark urine, or persistent abdominal pain."
    )

with st.expander("🫘 Kidney health"):
    st.markdown(
        "- Control blood pressure and blood sugar.\n"
        "- Drink enough water; avoid very high salt intake.\n"
        "- Avoid painkillers (NSAIDs) unless prescribed.\n"
        "- Seek care for swelling, reduced urine, or persistent fatigue."
    )

with st.expander("🫁 Lung health"):
    st.markdown(
        "- Do not smoke; avoid second-hand smoke.\n"
        "- Use masks in dusty environments.\n"
        "- Seek care for cough lasting more than 3 weeks, blood in sputum, or breathlessness."
    )

with st.expander("🎗️ Breast health"):
    st.markdown(
        "- Do regular self-breast awareness checks.\n"
        "- Follow screening advice for your age and risk.\n"
        "- Seek care for a new lump, skin changes, or nipple discharge."
    )

render_disclaimer()
