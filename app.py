"""
Multi-Disease Prediction System — Main Dashboard & Entry Point
"""
import datetime
import html
import json
import os
import sys

import pandas as pd
import streamlit as st

# Add project root to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.auth.auth_ui import current_user, require_login
from src.auth.storage import display_name, list_runs
from src.i18n import t
from src.utils.constants import APP_TITLE, DISEASE_METADATA
from src.utils.sidebar import render_sidebar
from src.utils.header import render_header
from src.utils.ui_components import (
    inject_custom_css,
    render_disclaimer,
    section_header,
)

st.set_page_config(
    page_title=f"{APP_TITLE} | Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
require_login()
render_sidebar()
render_header(page_key="home")

# Load live model metadata
model_stats = {}
for d_key in DISEASE_METADATA:
    meta_path = os.path.join(BASE_DIR, "models", d_key, "metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            model_stats[d_key] = json.load(f)
    else:
        model_stats[d_key] = {"model_name": "Trained Model", "accuracy": 0.0, "dataset_rows": 0}

recent_runs = list_runs(limit=50) if st.session_state.get("user") else []
avg_accuracy = (
    sum(m.get("accuracy", 0) for m in model_stats.values()) / len(model_stats) * 100
    if model_stats else 0
)
total_cohort_rows = sum(m.get("dataset_rows", 0) for m in model_stats.values())

user = current_user()
name = display_name(user) if user else ""
first_name = name.split()[0] if name else "there"
hour = datetime.datetime.now().hour
greeting = "Good morning" if hour < 12 else ("Good afternoon" if hour < 17 else "Good evening")

st.markdown(
    f"""
    <div class="app-hero">
        <div class="hero-eyebrow">👋 {html.escape(greeting)}, {html.escape(first_name)}</div>
        <div class="hero-title">{t('hero_title')}</div>
        <p class="hero-sub">{t('hero_sub')}</p>
        <div class="hero-tags">
            <span class="hero-tag">🔬 5 Disease Modules</span>
            <span class="hero-tag">🧠 Interpretable Decision Support</span>
            <span class="hero-tag">🔒 Private Diagnostic Records</span>
        </div>
    </div>
    <div class="stat-grid">
        <div class="stat-tile">
            <div class="stat-kicker">Training cohort</div>
            <div class="stat-value">{total_cohort_rows:,}</div>
            <div class="stat-hint">Records across the 5 datasets</div>
        </div>
        <div class="stat-tile">
            <div class="stat-kicker">Mean Accuracy</div>
            <div class="stat-value">{avg_accuracy:.1f}%</div>
            <div class="stat-hint">Across held-out test splits</div>
        </div>
        <div class="stat-tile">
            <div class="stat-kicker">Active Pipelines</div>
            <div class="stat-value">5</div>
            <div class="stat-hint">Serialized ML classification models</div>
        </div>
        <div class="stat-tile">
            <div class="stat-kicker">Diagnostic Runs</div>
            <div class="stat-value">{len(recent_runs)}</div>
            <div class="stat-hint">Saved in your secure session</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if recent_runs:
    section_header(t("recent_title"), "Your latest saved results.")
    tiles = []
    for run in recent_runs[:3]:
        res = run.get("result", {}) or {}
        disease = html.escape(str(run.get("disease", "")).replace("_", " "))
        label = html.escape(str(res.get("result_label", "N/A")))
        tiles.append(
            f'<div class="stat-tile"><div class="stat-kicker">{disease}</div>'
            f'<div class="stat-value" style="font-size:1.05rem;">{label}</div>'
            f'<div class="stat-hint">{res.get("confidence", 0)}% confidence</div></div>'
        )
    st.markdown(f'<div class="stat-grid">{"".join(tiles)}</div>', unsafe_allow_html=True)

section_header(t("modules_title"), t("modules_sub"))


def disease_card(col, icon, title, meta, key, page, desc, default_model):
    with col:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="module-top">
                    <div class="module-icon {key}">{icon}</div>
                    <div>
                        <div class="module-title">{title}</div>
                        <div style="margin-top:7px;">
                            <span class="pill model">{meta.get('model_name', default_model)}</span>
                            <span class="pill acc">{meta.get('accuracy', 0)*100:.1f}% acc</span>
                        </div>
                    </div>
                </div>
                <div class="module-desc">{desc}</div>
                """,
                unsafe_allow_html=True,
            )
            st.page_link(page, label=f"{t('start')} →")


row1 = st.columns(3)
disease_card(row1[0], "❤️", "Heart Disease", model_stats["heart"], "heart", "pages/1_Heart_Disease.py", DISEASE_METADATA["heart"]["short_desc"], "Logistic Regression")
disease_card(row1[1], "🫘", "Kidney Disease", model_stats["kidney"], "kidney", "pages/2_Kidney_Disease.py", DISEASE_METADATA["kidney"]["short_desc"], "Random Forest")
disease_card(row1[2], "🫀", "Liver Disease", model_stats["liver"], "liver", "pages/3_Liver_Disease.py", DISEASE_METADATA["liver"]["short_desc"], "Logistic Regression")

row2 = st.columns(2)
disease_card(row2[0], "🫁", "Lung Disease", model_stats["lung"], "lung", "pages/4_Lung_Disease.py", DISEASE_METADATA["lung"]["short_desc"], "KNN")
disease_card(row2[1], "🎗️", "Breast Cancer", model_stats["breast_cancer"], "breast", "pages/5_Breast_Cancer.py", DISEASE_METADATA["breast_cancer"]["short_desc"], "SVM")

st.write("")
section_header(t("workflow_title"), "Four steps from inputs to an explainable result.")
st.markdown(
    """
    <div class="steps">
        <div class="step">
            <div class="step-num">1</div>
            <div class="step-title">Enter clinical values</div>
            <div class="step-desc">Guided forms with units, normal ranges and validation.</div>
        </div>
        <div class="step">
            <div class="step-num">2</div>
            <div class="step-title">Feature pipeline</div>
            <div class="step-desc">Encoding, imputation and scaling fitted inside the model pipeline.</div>
        </div>
        <div class="step">
            <div class="step-num">3</div>
            <div class="step-title">Model inference</div>
            <div class="step-desc">The selected classifier returns a probability and risk band.</div>
        </div>
        <div class="step">
            <div class="step-num">4</div>
            <div class="step-title">Understand the result</div>
            <div class="step-desc">Confidence, contributing factors, guidance and a downloadable report.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander(f"📈 {t('metrics_title')} & benchmarks", expanded=False):
    metrics_rows = []
    for d_key, info in DISEASE_METADATA.items():
        m = model_stats.get(d_key, {})
        metrics_rows.append({
            "Disease module": f"{info['icon']} {info['name']}",
            "Algorithm": m.get("model_name", "N/A"),
            "Accuracy": f"{m.get('accuracy', 0)*100:.2f}%",
            "Precision": f"{m.get('precision', 0)*100:.2f}%",
            "Recall": f"{m.get('recall', 0)*100:.2f}%",
            "F1": f"{m.get('f1_score', 0)*100:.2f}%",
            "ROC-AUC": f"{m.get('roc_auc', 0)*100:.2f}%",
            "Samples": f"{m.get('dataset_rows', 0):,}",
        })
    st.dataframe(pd.DataFrame(metrics_rows), width="stretch", hide_index=True)
    st.caption("Kidney accuracy is dataset-specific: CKD markers are strongly separable in the UCI cohort.")

st.write("")
section_header(t("team_title"), "Academic project · Group 17")
st.markdown(
    """
    <div class="team-panel">
        <div>
            <div class="team-label">Project guide</div>
            <div class="team-name">Dr. Manjunath R</div>
            <div class="team-desc" style="font-size:.82rem;color:#64748b;">Professor & HOD</div>
            <div class="team-label" style="margin-top:16px;">Institution</div>
            <div class="team-name" style="font-size:.88rem;">Academic ML research prototype</div>
        </div>
        <div>
            <div class="team-label">Team</div>
            <div class="team-list">
                M Kushala · 1RI23CS078<br>
                Prajwal Aravind D M · 1RI23CS108<br>
                Sameeksha M G · 1RI23CS128<br>
                Shiva Prakash T R · 1RI23CS134
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

render_disclaimer()
st.caption(f"🩺 {APP_TITLE} · Academic screening prototype · Not a medical device")
