"""Clinical reference ranges for input fields (educational)."""
CLINICAL_REFERENCES = {
    "heart": {
        "Resting BP (mm Hg)": "<120 normal, 120-139 elevated, >=140 high",
        "Cholesterol (mg/dl)": "<200 desirable, 200-239 borderline, >=240 high",
        "Max HR (bpm)": "220 - age (approx.)",
        "ST Depression (mm)": "0 normal, >0 abnormal",
    },
    "kidney": {
        "Serum Creatinine (mg/dl)": "0.6-1.3 (M), 0.5-1.1 (F)",
        "Blood Urea (mg/dl)": "7-20",
        "Hemoglobin (g/dl)": "13.5-17.5 (M), 12.0-15.5 (F)",
        "Sodium (mEq/L)": "135-145",
        "Potassium (mEq/L)": "3.5-5.0",
    },
    "liver": {
        "Total Bilirubin (mg/dl)": "0.2-1.2",
        "Direct Bilirubin (mg/dl)": "0.0-0.3",
        "ALT/SGPT (IU/L)": "7-56",
        "AST/SGOT (IU/L)": "10-40",
        "ALP (IU/L)": "44-147",
        "Albumin (g/dl)": "3.5-5.0",
    },
    "lung": {
        "Age (years)": "Risk rises after 50",
        "Smoking": "Major modifiable risk factor",
    },
    "breast_cancer": {
        "Mean Radius (mm)": "Typical benign ~11-13, malignant ~17-22",
        "Mean Area (mm²)": "Higher values suggest malignancy",
    },
}


def render_clinical_references(disease):
    import streamlit as st
    refs = CLINICAL_REFERENCES.get(disease)
    if not refs:
        return
    with st.expander("📏 Clinical Reference Ranges", expanded=False):
        for k, v in refs.items():
            st.markdown(f"- **{k}**: {v}")
