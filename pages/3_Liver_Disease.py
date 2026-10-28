"""
Liver Disease Prediction Page — Multi-Disease Prediction System
"""
import streamlit as st
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.utils.constants import LIVER_FIELDS, DISEASE_METADATA
from src.utils.ui_components import (
    inject_custom_css,
    page_header,
    render_disclaimer,
    render_model_info_expander,
    render_prediction_result,
    render_empty_prediction_placeholder,
)
from src.prediction.predict import predict_disease
from src.auth.auth_ui import require_login
from src.auth.storage import get_last_inputs, save_diagnosis_run
from src.utils.sidebar import render_sidebar
from src.i18n import t
from src.utils.header import render_header
from src.utils.clinical_refs import render_clinical_references

st.set_page_config(
    page_title="Liver Disease Prediction | MDPS",
    page_icon="🫀",
    layout="wide"
)

inject_custom_css()

require_login()
render_sidebar()
render_header(page_key="liver")

# Header
page_header(
    "🫀",
    t("page_liver_title"),
    t("page_liver_sub"),
)

render_disclaimer(full=True)

if "liver_data" not in st.session_state:
    _last = get_last_inputs("liver") if st.session_state.get("user") else None
    st.session_state.liver_data = _last if _last else {k: v["default"] for k, v in LIVER_FIELDS.items()}
    if _last:
        st.toast("Resumed your last saved liver inputs.")

col_form, col_panel = st.columns([1.3, 1.0], gap="large")

with col_form:
    st.markdown("##### ⚡ Quick Demonstration Presets")
    c_preset1, c_preset2, c_preset3 = st.columns([1, 1, 0.7])
    with c_preset1:
        if st.button("🟢 Low Risk Sample", width="stretch"):
            st.session_state.liver_data = {
                "Age": 28, "Gender": "Female", "TB": 0.7, "DB": 0.2, "Alkphos": 155,
                "Sgpt": 22, "Sgot": 24, "TP": 7.3, "ALB": 4.0, "A_G_Ratio": 1.2
            }
            st.rerun()

    with c_preset2:
        if st.button("🔴 High Risk Sample", width="stretch"):
            st.session_state.liver_data = {
                "Age": 58, "Gender": "Male", "TB": 6.8, "DB": 3.4, "Alkphos": 490,
                "Sgpt": 145, "Sgot": 160, "TP": 5.6, "ALB": 2.4, "A_G_Ratio": 0.7
            }
            st.rerun()

    with c_preset3:
        if st.button("🔄 Reset", width="stretch"):
            st.session_state.liver_data = {k: v["default"] for k, v in LIVER_FIELDS.items()}
            st.rerun()

    with st.form("liver_form"):
        st.markdown("#### 📋 Hepatic Diagnostic Markers")

        tab1, tab2, tab3 = st.tabs(['Demographics & Bilirubin', 'Hepatic Enzymes', 'Proteins & Ratios'])

        with tab1:
            st.markdown("**1. Patient Demographics & Bilirubin**")
            Age = st.number_input("Age (years)", min_value=4, max_value=95, value=int(st.session_state.liver_data.get("Age", 45)))
            Gender = st.selectbox("Gender", options=["Male", "Female"], index=["Male", "Female"].index(st.session_state.liver_data.get("Gender", "Male")))
            TB = st.number_input("Total Bilirubin - TB (mg/dl)", min_value=0.4, max_value=75.0, value=float(st.session_state.liver_data.get("TB", 1.2)), step=0.1, help="Normal reference: 0.2 - 1.2 mg/dl")
            DB = st.number_input("Direct Bilirubin - DB (mg/dl)", min_value=0.1, max_value=20.0, value=float(st.session_state.liver_data.get("DB", 0.4)), step=0.1, help="Normal reference: 0.0 - 0.3 mg/dl")

        with tab2:
            st.markdown("**2. Hepatic Enzymes**")
            Alkphos = st.number_input("Alkaline Phosphatase - ALP (IU/L)", min_value=60, max_value=2200, value=int(st.session_state.liver_data.get("Alkphos", 200)), help="Normal reference: 44 - 147 IU/L")
            Sgpt = st.number_input("Alamine Aminotransferase - ALT / SGPT (IU/L)", min_value=10, max_value=2000, value=int(st.session_state.liver_data.get("Sgpt", 35)), help="Normal reference: 7 - 56 IU/L")
            Sgot = st.number_input("Aspartate Aminotransferase - AST / SGOT (IU/L)", min_value=10, max_value=5000, value=int(st.session_state.liver_data.get("Sgot", 40)), help="Normal reference: 10 - 40 IU/L")

        with tab3:
            st.markdown("**3. Serum Proteins & Ratios**")
            TP = st.number_input("Total Proteins - TP (g/dl)", min_value=2.5, max_value=10.0, value=float(st.session_state.liver_data.get("TP", 6.8)), step=0.1, help="Normal reference: 6.0 - 8.3 g/dl")
            ALB = st.number_input("Albumin - ALB (g/dl)", min_value=0.8, max_value=6.0, value=float(st.session_state.liver_data.get("ALB", 3.4)), step=0.1, help="Normal reference: 3.5 - 5.0 g/dl")
            A_G_Ratio = st.number_input("Albumin and Globulin Ratio (A/G)", min_value=0.3, max_value=3.0, value=float(st.session_state.liver_data.get("A_G_Ratio", 1.0)), step=0.05, help="Normal reference: 1.0 - 2.2")

        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button(t("run_liver"), type="primary", width="stretch")

    if submit_btn:
        user_payload = {
            "Age": Age,
            "Gender": Gender,
            "TB": TB,
            "DB": DB,
            "Alkphos": Alkphos,
            "Sgpt": Sgpt,
            "Sgot": Sgot,
            "TP": TP,
            "ALB": ALB,
            "A_G_Ratio": A_G_Ratio
        }

        with st.spinner("Analyzing hepatic enzyme concentrations..."):
            prediction_res = predict_disease("liver", user_payload)
            st.session_state.last_prediction = {"disease": "liver", "result": prediction_res}
            save_diagnosis_run("liver", user_payload, prediction_res)
            st.rerun()

with col_panel:
    last_pred = st.session_state.get("last_prediction")
    if last_pred and last_pred.get("disease") == "liver":
        render_prediction_result(last_pred["result"])
    else:
        render_empty_prediction_placeholder("liver")

    with st.expander("🩺 Clinical Biomarker Reference Intervals"):
        render_clinical_references("liver")

st.markdown("---")
render_model_info_expander("liver")
