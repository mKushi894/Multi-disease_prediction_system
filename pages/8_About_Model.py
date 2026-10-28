"""
About the model page — datasets, algorithms, metrics, limitations.
"""
import streamlit as st
import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.auth.auth_ui import require_login
from src.utils.constants import DISEASE_METADATA
from src.utils.ui_components import inject_custom_css, page_header, render_disclaimer
from src.utils.sidebar import render_sidebar
from src.i18n import t
from src.utils.header import render_header

st.set_page_config(page_title="About the Model | MDPS", page_icon="🧠", layout="wide")
inject_custom_css()
require_login()
render_sidebar()
render_header(page_key="about")

page_header(
    "🧠",
    t("page_about_title"),
    t("page_about_sub"),
)

rows = []
for key, info in DISEASE_METADATA.items():
    meta_path = os.path.join(BASE_DIR, "models", key, "metadata.json")
    if not os.path.exists(meta_path):
        continue
    with open(meta_path, "r") as f:
        meta = json.load(f)
    rows.append({
        "Disease": info["name"],
        "Dataset rows": meta.get("dataset_rows", 0),
        "Algorithm": meta.get("model_name", "N/A"),
        "Accuracy": f"{meta.get('accuracy', 0)*100:.2f}%",
        "F1": f"{meta.get('f1_score', 0)*100:.2f}%",
        "ROC-AUC": f"{meta.get('roc_auc', 0)*100:.2f}%",
    })

st.dataframe(rows, width="stretch", hide_index=True)

st.markdown("### 📌 Limitations")
st.markdown(
    "- Predictions are statistical estimates from research datasets, not a diagnosis.\n"
    "- Datasets are small and may not represent every population.\n"
    "- Kidney markers are strongly separable in the UCI cohort, so 100% test accuracy is dataset-specific.\n"
    "- The lung module uses survey/lifestyle data, not imaging.\n"
    "- Always consult a qualified clinician for medical decisions."
)

render_disclaimer()
