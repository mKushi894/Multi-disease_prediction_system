"""
Heart Disease Prediction Page — Multi-Disease Prediction System
"""
import streamlit as st
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.utils.constants import HEART_FIELDS, DISEASE_METADATA
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
    page_title="Heart Disease Prediction | MDPS",
    page_icon="❤️",
    layout="wide"
)

inject_custom_css()

require_login()
render_sidebar()
render_header(page_key="heart")

# Header
page_header(
    "❤️",
    t("page_heart_title"),
    t("page_heart_sub"),
)

render_disclaimer(full=True)

if "heart_data" not in st.session_state:
    _last = get_last_inputs("heart") if st.session_state.get("user") else None
    st.session_state.heart_data = _last if _last else {k: v["default"] for k, v in HEART_FIELDS.items()}
    if _last:
        st.toast("Resumed your last saved heart inputs.")

col_form, col_panel = st.columns([1.3, 1.0], gap="large")

with col_form:
    st.markdown("##### ⚡ Quick Demonstration Presets")
    c_preset1, c_preset2, c_preset3 = st.columns([1, 1, 0.7])
    with c_preset1:
        if st.button("🟢 Low Risk Sample", width="stretch"):
            st.session_state.heart_data = {
                "age": 35, "sex": "Female", "cp": "Typical Angina", "trestbps": 118, "chol": 182,
                "fbs": "No", "restecg": "Normal", "thalach": 172, "exang": "No", "oldpeak": 0.0,
                "slope": "Upsloping", "ca": 0, "thal": "Normal"
            }
            st.rerun()

    with c_preset2:
        if st.button("🔴 High Risk Sample", width="stretch"):
            st.session_state.heart_data = {
                "age": 62, "sex": "Male", "cp": "Asymptomatic", "trestbps": 160, "chol": 290,
                "fbs": "Yes", "restecg": "Left Ventricular Hypertrophy", "thalach": 108, "exang": "Yes", "oldpeak": 3.2,
                "slope": "Downsloping", "ca": 2, "thal": "Reversible Defect"
            }
            st.rerun()

    with c_preset3:
        if st.button("🔄 Reset", width="stretch"):
            st.session_state.heart_data = {k: v["default"] for k, v in HEART_FIELDS.items()}
            st.rerun()

    with st.form("heart_form"):
        st.markdown("#### 📋 Clinical Input Parameters")

        tab1, tab2, tab3 = st.tabs(['Demographics & Vitals', 'Symptoms & Metabolic', 'Stress & Diagnostics'])

        with tab1:
            st.markdown("**1. Demographics & Vitals**")
            age = st.number_input("Age (years)", min_value=18, max_value=100, value=int(st.session_state.heart_data.get("age", 54)), help="Patient age in years")
            sex = st.selectbox("Biological Sex", options=["Male", "Female"], index=["Male", "Female"].index(st.session_state.heart_data.get("sex", "Male")))
            trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=80, max_value=200, value=int(st.session_state.heart_data.get("trestbps", 130)), help="Resting BP upon admission (Normal < 120)")
            chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=100, max_value=600, value=int(st.session_state.heart_data.get("chol", 240)), help="Total serum cholesterol (Desirable < 200)")

        with tab2:
            st.markdown("**2. Symptoms & Metabolic**")
            cp = st.selectbox("Chest Pain Type (CP)", options=["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"], index=["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"].index(st.session_state.heart_data.get("cp", "Typical Angina")))
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.heart_data.get("fbs", "No")))
            restecg = st.selectbox("Resting ECG Result", options=["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"], index=["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"].index(st.session_state.heart_data.get("restecg", "Normal")))
            thalach = st.number_input("Max Heart Rate Achieved (bpm)", min_value=60, max_value=220, value=int(st.session_state.heart_data.get("thalach", 150)))

        with tab3:
            st.markdown("**3. Stress Test & Diagnostics**")
            exang = st.selectbox("Exercise-Induced Angina", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.heart_data.get("exang", "No")))
            oldpeak = st.number_input("ST Depression (Oldpeak)", min_value=0.0, max_value=6.5, value=float(st.session_state.heart_data.get("oldpeak", 1.0)), step=0.1)
            slope = st.selectbox("Slope of Peak Exercise ST", options=["Upsloping", "Flat", "Downsloping"], index=["Upsloping", "Flat", "Downsloping"].index(st.session_state.heart_data.get("slope", "Flat")))
            ca = st.number_input("Major Vessels Colored by Fluoroscopy (0-4)", min_value=0, max_value=4, value=int(st.session_state.heart_data.get("ca", 0)))
            thal = st.selectbox("Thalassemia Status", options=["Normal", "Fixed Defect", "Reversible Defect"], index=["Normal", "Fixed Defect", "Reversible Defect"].index(st.session_state.heart_data.get("thal", "Normal")))

        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button(t("run_heart"), type="primary", width="stretch")

    if submit_btn:
        user_payload = {
            "age": age,
            "sex": sex,
            "cp": cp,
            "trestbps": trestbps,
            "chol": chol,
            "fbs": fbs,
            "restecg": restecg,
            "thalach": thalach,
            "exang": exang,
            "oldpeak": oldpeak,
            "slope": slope,
            "ca": ca,
            "thal": thal
        }

        with st.spinner("Analyzing cardiovascular biomarker indicators..."):
            prediction_res = predict_disease("heart", user_payload)
            st.session_state.last_prediction = {"disease": "heart", "result": prediction_res}
            save_diagnosis_run("heart", user_payload, prediction_res)
            st.rerun()

with col_panel:
    last_pred = st.session_state.get("last_prediction")
    if last_pred and last_pred.get("disease") == "heart":
        render_prediction_result(last_pred["result"])
    else:
        render_empty_prediction_placeholder("heart")

    with st.expander("🩺 Clinical Biomarker Reference Intervals"):
        render_clinical_references("heart")

st.markdown("---")
render_model_info_expander("heart")
