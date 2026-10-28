"""
Kidney Disease Prediction Page — Multi-Disease Prediction System
"""
import streamlit as st
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.utils.constants import KIDNEY_FIELDS, DISEASE_METADATA
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
    page_title="Kidney Disease Prediction | MDPS",
    page_icon="🫘",
    layout="wide"
)

inject_custom_css()

require_login()
render_sidebar()
render_header(page_key="kidney")

# Header
page_header(
    "🫘",
    t("page_kidney_title"),
    t("page_kidney_sub"),
)

render_disclaimer(full=True)

if "kidney_data" not in st.session_state:
    _last = get_last_inputs("kidney") if st.session_state.get("user") else None
    st.session_state.kidney_data = _last if _last else {k: v["default"] for k, v in KIDNEY_FIELDS.items()}
    if _last:
        st.toast("Resumed your last saved kidney inputs.")

col_form, col_panel = st.columns([1.3, 1.0], gap="large")

with col_form:
    st.markdown("##### ⚡ Quick Demonstration Presets")
    c_preset1, c_preset2, c_preset3 = st.columns([1, 1, 0.7])
    with c_preset1:
        if st.button("🟢 Low Risk Sample", width="stretch"):
            st.session_state.kidney_data = {
                "age": 42, "bp": 75, "sg": "1.025", "al": "0", "su": "0", "rbc": "Normal",
                "pc": "Normal", "pcc": "Not Present", "ba": "Not Present", "bgr": 95,
                "bu": 24.0, "sc": 0.8, "sod": 140.0, "pot": 4.1, "hemo": 15.6, "pcv": 46,
                "wbcc": 6800, "rbcc": 5.4, "htn": "No", "dm": "No", "cad": "No", "appet": "Good",
                "pe": "No", "ane": "No"
            }
            st.rerun()

    with c_preset2:
        if st.button("🔴 High Risk Sample", width="stretch"):
            st.session_state.kidney_data = {
                "age": 64, "bp": 90, "sg": "1.010", "al": "3", "su": "2", "rbc": "Abnormal",
                "pc": "Abnormal", "pcc": "Present", "ba": "Present", "bgr": 240,
                "bu": 115.0, "sc": 4.2, "sod": 129.0, "pot": 5.6, "hemo": 8.6, "pcv": 27,
                "wbcc": 13500, "rbcc": 3.2, "htn": "Yes", "dm": "Yes", "cad": "Yes", "appet": "Poor",
                "pe": "Yes", "ane": "Yes"
            }
            st.rerun()

    with c_preset3:
        if st.button("🔄 Reset", width="stretch"):
            st.session_state.kidney_data = {k: v["default"] for k, v in KIDNEY_FIELDS.items()}
            st.rerun()

    with st.form("kidney_form"):
        st.markdown("#### 📋 Clinical Biomarkers & History")

        tab1, tab2, tab3 = st.tabs(['Vitals & Urinalysis', 'Blood Chemistry', 'Conditions'])

        with tab1:
            st.markdown("**1. Vitals & Urinalysis**")
            age = st.number_input("Age (years)", min_value=1, max_value=100, value=int(st.session_state.kidney_data.get("age", 50)), help="Risk of CKD rises with age.")
            bp = st.number_input("Blood Pressure (mm Hg)", min_value=50, max_value=180, value=int(st.session_state.kidney_data.get("bp", 80)), help="Normal: <120/80 mmHg.")
            sg = st.selectbox("Specific Gravity", options=["1.005", "1.010", "1.015", "1.020", "1.025"], index=["1.005", "1.010", "1.015", "1.020", "1.025"].index(str(st.session_state.kidney_data.get("sg", "1.020"))))
            al = st.selectbox("Albumin (0 to 5)", options=["0", "1", "2", "3", "4", "5"], index=["0", "1", "2", "3", "4", "5"].index(str(st.session_state.kidney_data.get("al", "0"))))
            su = st.selectbox("Sugar (0 to 5)", options=["0", "1", "2", "3", "4", "5"], index=["0", "1", "2", "3", "4", "5"].index(str(st.session_state.kidney_data.get("su", "0"))))
            rbc = st.selectbox("Red Blood Cells in Urine", options=["Normal", "Abnormal"], index=["Normal", "Abnormal"].index(st.session_state.kidney_data.get("rbc", "Normal")))
            pc = st.selectbox("Pus Cells in Urine", options=["Normal", "Abnormal"], index=["Normal", "Abnormal"].index(st.session_state.kidney_data.get("pc", "Normal")))
            pcc = st.selectbox("Pus Cell Clumps", options=["Not Present", "Present"], index=["Not Present", "Present"].index(st.session_state.kidney_data.get("pcc", "Not Present")))
            ba = st.selectbox("Bacteria in Urine", options=["Not Present", "Present"], index=["Not Present", "Present"].index(st.session_state.kidney_data.get("ba", "Not Present")))

        with tab2:
            st.markdown("**2. Blood Chemistry & Renal Markers**")
            bgr = st.number_input("Blood Glucose Random (mg/dl)", min_value=20, max_value=500, value=int(st.session_state.kidney_data.get("bgr", 120)), help="Normal fasting: 70-99 mg/dl.")
            bu = st.number_input("Blood Urea (mg/dl)", min_value=1.5, max_value=400.0, value=float(st.session_state.kidney_data.get("bu", 40.0)), step=1.0, help="Normal: 7-20 mg/dl.")
            sc = st.number_input("Serum Creatinine (mg/dl)", min_value=0.4, max_value=80.0, value=float(st.session_state.kidney_data.get("sc", 1.1)), step=0.1, help="Normal: 0.6-1.3 (M), 0.5-1.1 (F) mg/dl.")
            sod = st.number_input("Sodium (mEq/L)", min_value=4.5, max_value=165.0, value=float(st.session_state.kidney_data.get("sod", 138.0)), step=0.5)
            pot = st.number_input("Potassium (mEq/L)", min_value=2.5, max_value=50.0, value=float(st.session_state.kidney_data.get("pot", 4.2)), step=0.1)
            hemo = st.number_input("Hemoglobin (g/dl)", min_value=3.0, max_value=18.0, value=float(st.session_state.kidney_data.get("hemo", 14.5)), step=0.1, help="Normal: 13.5-17.5 (M), 12.0-15.5 (F) g/dl.")
            pcv = st.number_input("Packed Cell Volume (%)", min_value=9, max_value=55, value=int(st.session_state.kidney_data.get("pcv", 42)))
            wbcc = st.number_input("White Blood Cell Count (cells/cumm)", min_value=2000, max_value=27000, value=int(st.session_state.kidney_data.get("wbcc", 8000)))
            rbcc = st.number_input("Red Blood Cell Count (m/cumm)", min_value=2.0, max_value=8.0, value=float(st.session_state.kidney_data.get("rbcc", 5.0)), step=0.1)

        with tab3:
            st.markdown("**3. Medical Conditions & Symptoms**")
            htn = st.selectbox("Hypertension", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.kidney_data.get("htn", "No")))
            dm = st.selectbox("Diabetes Mellitus", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.kidney_data.get("dm", "No")))
            cad = st.selectbox("Coronary Artery Disease", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.kidney_data.get("cad", "No")))
            appet = st.selectbox("Appetite", options=["Good", "Poor"], index=["Good", "Poor"].index(st.session_state.kidney_data.get("appet", "Good")))
            pe = st.selectbox("Pedal Edema (Foot Swelling)", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.kidney_data.get("pe", "No")))
            ane = st.selectbox("Anemia Diagnosed", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.kidney_data.get("ane", "No")))

        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button(t("run_kidney"), type="primary", width="stretch")

    if submit_btn:
        user_payload = {
            "age": age, "bp": bp, "sg": sg, "al": al, "su": su,
            "rbc": rbc, "pc": pc, "pcc": pcc, "ba": ba,
            "bgr": bgr, "bu": bu, "sc": sc, "sod": sod, "pot": pot,
            "hemo": hemo, "pcv": pcv, "wbcc": wbcc, "rbcc": rbcc,
            "htn": htn, "dm": dm, "cad": cad, "appet": appet, "pe": pe, "ane": ane
        }

        with st.spinner("Processing renal diagnostic profile..."):
            prediction_res = predict_disease("kidney", user_payload)
            st.session_state.last_prediction = {"disease": "kidney", "result": prediction_res}
            save_diagnosis_run("kidney", user_payload, prediction_res)
            st.rerun()

with col_panel:
    last_pred = st.session_state.get("last_prediction")
    if last_pred and last_pred.get("disease") == "kidney":
        render_prediction_result(last_pred["result"])
    else:
        render_empty_prediction_placeholder("kidney")

    with st.expander("🩺 Clinical Biomarker Reference Intervals"):
        render_clinical_references("kidney")

st.markdown("---")
render_model_info_expander("kidney")
