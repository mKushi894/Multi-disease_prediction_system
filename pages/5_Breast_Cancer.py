"""
Breast Cancer Prediction Page — Multi-Disease Prediction System
"""
import streamlit as st
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.utils.constants import BREAST_CANCER_FIELDS, DISEASE_METADATA
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
    page_title="Breast Cancer Prediction | MDPS",
    page_icon="🎗️",
    layout="wide"
)

inject_custom_css()

require_login()
render_sidebar()
render_header(page_key="breast")

# Header
page_header(
    "🎗️",
    t("page_breast_title"),
    t("page_breast_sub"),
)

render_disclaimer(full=True)

if "bc_data" not in st.session_state:
    _last = get_last_inputs("breast_cancer") if st.session_state.get("user") else None
    st.session_state.bc_data = _last if _last else {k: v["default"] for k, v in BREAST_CANCER_FIELDS.items()}
    if _last:
        st.toast("Resumed your last saved breast cancer inputs.")

col_form, col_panel = st.columns([1.3, 1.0], gap="large")

with col_form:
    st.markdown("##### ⚡ Quick Demonstration Presets")
    c_preset1, c_preset2, c_preset3 = st.columns([1, 1, 0.7])
    with c_preset1:
        if st.button("🟢 Benign Sample", width="stretch"):
            st.session_state.bc_data = {
                "mean_radius": 11.8, "mean_texture": 16.2, "mean_perimeter": 75.8, "mean_area": 427.0,
                "mean_smoothness": 0.086, "mean_compactness": 0.058, "mean_concavity": 0.024,
                "mean_concave_points": 0.018, "mean_symmetry": 0.165, "mean_fractal_dimension": 0.059
            }
            st.rerun()

    with c_preset2:
        if st.button("🔴 Malignant Sample", width="stretch"):
            st.session_state.bc_data = {
                "mean_radius": 20.6, "mean_texture": 25.5, "mean_perimeter": 138.0, "mean_area": 1320.0,
                "mean_smoothness": 0.118, "mean_compactness": 0.235, "mean_concavity": 0.280,
                "mean_concave_points": 0.145, "mean_symmetry": 0.240, "mean_fractal_dimension": 0.078
            }
            st.rerun()

    with c_preset3:
        if st.button("🔄 Reset", width="stretch"):
            st.session_state.bc_data = {k: v["default"] for k, v in BREAST_CANCER_FIELDS.items()}
            st.rerun()

    with st.form("breast_cancer_form"):
        st.markdown("#### 📋 Fine Needle Aspirate (FNA) Nuclei Measurements")

        tab1, tab2, tab3 = st.tabs(['Dimensions', 'Texture', 'Contour & Geometry'])

        with tab1:
            st.markdown("**1. Nucleus Dimensions & Size**")
            mean_radius = st.number_input("Mean Radius (mm)", min_value=6.0, max_value=30.0, value=float(st.session_state.bc_data.get("mean_radius", 14.1)), step=0.1, help="Mean of distances from center to contour points")
            mean_perimeter = st.number_input("Mean Perimeter (mm)", min_value=40.0, max_value=190.0, value=float(st.session_state.bc_data.get("mean_perimeter", 92.0)), step=0.5, help="Nuclear boundary perimeter")
            mean_area = st.number_input("Mean Area (mm²)", min_value=140.0, max_value=2500.0, value=float(st.session_state.bc_data.get("mean_area", 654.0)), step=1.0, help="Total nuclear surface area")

        with tab2:
            st.markdown("**2. Surface Texture & Smoothness**")
            mean_texture = st.number_input("Mean Texture", min_value=9.0, max_value=40.0, value=float(st.session_state.bc_data.get("mean_texture", 19.3)), step=0.1, help="Standard deviation of gray-scale values")
            mean_smoothness = st.number_input("Mean Smoothness", min_value=0.05, max_value=0.16, value=float(st.session_state.bc_data.get("mean_smoothness", 0.096)), step=0.001, format="%.4f", help="Local variation in radius lengths")
            mean_compactness = st.number_input("Mean Compactness", min_value=0.02, max_value=0.35, value=float(st.session_state.bc_data.get("mean_compactness", 0.104)), step=0.001, format="%.4f", help="Perimeter^2 / area - 1.0")

        with tab3:
            st.markdown("**3. Nuclear Contour & Geometry**")
            mean_concavity = st.number_input("Mean Concavity", min_value=0.0, max_value=0.45, value=float(st.session_state.bc_data.get("mean_concavity", 0.088)), step=0.001, format="%.4f", help="Severity of concave portions of contour")
            mean_concave_points = st.number_input("Mean Concave Points", min_value=0.0, max_value=0.20, value=float(st.session_state.bc_data.get("mean_concave_points", 0.048)), step=0.001, format="%.4f", help="Number of concave portions of the contour")
            mean_symmetry = st.number_input("Mean Symmetry", min_value=0.10, max_value=0.30, value=float(st.session_state.bc_data.get("mean_symmetry", 0.181)), step=0.001, format="%.4f", help="Symmetry score of cell nucleus")
            mean_fractal_dimension = st.number_input("Mean Fractal Dimension", min_value=0.05, max_value=0.10, value=float(st.session_state.bc_data.get("mean_fractal_dimension", 0.062)), step=0.001, format="%.4f", help="Coastline approximation - 1")

        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button(t("run_breast"), type="primary", width="stretch")

    if submit_btn:
        user_payload = {
            "mean_radius": mean_radius,
            "mean_texture": mean_texture,
            "mean_perimeter": mean_perimeter,
            "mean_area": mean_area,
            "mean_smoothness": mean_smoothness,
            "mean_compactness": mean_compactness,
            "mean_concavity": mean_concavity,
            "mean_concave_points": mean_concave_points,
            "mean_symmetry": mean_symmetry,
            "mean_fractal_dimension": mean_fractal_dimension
        }

        with st.spinner("Analyzing fine needle aspirate morphology..."):
            prediction_res = predict_disease("breast_cancer", user_payload)
            st.session_state.last_prediction = {"disease": "breast_cancer", "result": prediction_res}
            save_diagnosis_run("breast_cancer", user_payload, prediction_res)
            st.rerun()

with col_panel:
    last_pred = st.session_state.get("last_prediction")
    if last_pred and last_pred.get("disease") == "breast_cancer":
        render_prediction_result(last_pred["result"])
    else:
        render_empty_prediction_placeholder("breast_cancer")

    with st.expander("🩺 Clinical Biomarker Reference Intervals"):
        render_clinical_references("breast_cancer")

st.markdown("---")
render_model_info_expander("breast_cancer")
