"""
Diagnosis history page — Multi-Disease Prediction System
"""
import streamlit as st
import os
import sys
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.auth.auth_ui import require_login
from src.auth.storage import list_runs, delete_run, clear_all_runs
from src.utils.ui_components import inject_custom_css, page_header, render_disclaimer
from src.utils.sidebar import render_sidebar
from src.i18n import t
from src.utils.header import render_header
from src.utils.constants import DISEASE_METADATA
from src.utils.reports import (
    format_timestamp_friendly,
    generate_diagnostic_report_pdf,
    generate_diagnostic_report_text,
    REPORT_FIELD_DEFINITIONS,
    _format_observed_value,
)

st.set_page_config(page_title="My History | MDPS", page_icon="📜", layout="wide")
inject_custom_css()

require_login()
render_sidebar()
render_header(page_key="history")

page_header("📜", t("page_history_title"), t("page_history_sub"))
render_disclaimer()

runs = list_runs()

if not runs:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">📜</div>
            <div class="empty-title">No saved screenings yet</div>
            <div class="empty-sub">Run any prediction while signed in and it will appear here with its inputs, clinical assessment, and downloadable PDF reports.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("app.py", label="← Back to dashboard", icon="🏠")
    st.stop()

# Summary Metrics Bar
distinct_diseases = len({str(r.get("disease", "")).lower() for r in runs if r.get("disease")})
first_created = runs[0].get("created_at") if runs else None
formatted_last = format_timestamp_friendly(first_created) if first_created else "—"

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Screenings", len(runs))
with c2:
    st.metric("Organs / Modules Screened", distinct_diseases)
with c3:
    st.metric("Most Recent Screening", formatted_last)

st.markdown("<br>", unsafe_allow_html=True)

# Filter Controls & Actions Bar
disease_names_set = sorted({
    DISEASE_METADATA.get(str(r.get("disease", "")).lower(), {}).get(
        "name", str(r.get("disease", "")).replace("_", " ").title()
    )
    for r in runs
    if r.get("disease")
})
disease_options = ["All Screening Modules"] + disease_names_set
c_sel, c_clear = st.columns([3, 1.2])
with c_sel:
    selected_option = st.selectbox("Filter History by Module", disease_options, label_visibility="visible")
with c_clear:
    st.write("")
    st.write("")
    with st.popover("🗑️ Clear History", help="Delete all diagnostic screening records"):
        st.markdown("**Clear all history?**")
        st.caption("This will permanently delete all recorded patient screenings and diagnostic reports.")
        if st.button("Confirm Clear All", key="confirm_clear_all_btn", type="primary", use_container_width=True):
            clear_all_runs()
            st.toast("Screening history cleared.", icon="🗑️")
            st.rerun()

if selected_option == "All Screening Modules":
    filtered_runs = runs
else:
    filtered_runs = [
        r
        for r in runs
        if DISEASE_METADATA.get(str(r.get("disease", "")).lower(), {}).get(
            "name", str(r.get("disease", "")).replace("_", " ").title()
        )
        == selected_option
    ]

page_map = {
    "heart": "pages/1_Heart_Disease.py",
    "kidney": "pages/2_Kidney_Disease.py",
    "liver": "pages/3_Liver_Disease.py",
    "lung": "pages/4_Lung_Disease.py",
    "breast_cancer": "pages/5_Breast_Cancer.py",
}

for r in filtered_runs:
    disease = str(r.get("disease", "")).lower()
    meta = DISEASE_METADATA.get(disease, {})
    icon = meta.get("icon", "🩺")
    name = meta.get("name", disease.replace("_", " ").title())

    res = r.get("result", {}) or {}
    is_pos = bool(res.get("is_positive", False))
    label = res.get("result_label", "Screening Complete")
    conf = res.get("confidence")
    risk_level = res.get("risk_level", "High Risk" if is_pos else "Low Risk")
    created_str = format_timestamp_friendly(r.get("created_at"))
    inputs = r.get("inputs") or res.get("user_inputs") or res.get("input_features") or {}

    with st.container(border=True):
        # Header Row
        col_title, col_action = st.columns([3.2, 1.2])
        with col_title:
            status_chip = "🔴 **High Risk**" if is_pos else "🟢 **Low Risk**"
            conf_display = f" · **{conf}%** confidence" if conf is not None else ""
            st.markdown(f"### {icon} {name}")
            st.markdown(f"{status_chip} &bull; **{label}**{conf_display}")
            st.caption(f"🕒 Screened on **{created_str}**")
        with col_action:
            if disease in page_map:
                st.page_link(page_map[disease], label=f"Open {name} Module →")

        # Recommendation callout
        rec = res.get("recommendation")
        if rec:
            st.info(f"**Clinical Finding / Guidance:** {rec}")

        # Metrics Row
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Risk Classification", risk_level)
        with m2:
            st.metric("Risk Probability", f"{res.get('probability_positive', 'N/A')}%")
        with m3:
            st.metric("Normal Baseline", f"{res.get('probability_negative', 'N/A')}%")

        # Clinical Parameters Expander
        if inputs:
            with st.expander("📋 View Recorded Clinical Parameters & Biomarkers", expanded=False):
                field_defs = REPORT_FIELD_DEFINITIONS.get(disease, {})
                table_rows = []
                for k, v in inputs.items():
                    fdef = field_defs.get(k) or field_defs.get(str(k).replace(" ", "_")) or {}
                    label_name = fdef.get("label", str(k).replace("_", " ").title())
                    table_rows.append({
                        "Parameter / Biomarker": label_name,
                        "Observed Value": _format_observed_value(v, k, disease),
                        "Standard Unit": fdef.get("unit", "--"),
                        "Reference Interval": fdef.get("ref", "--"),
                    })
                st.dataframe(pd.DataFrame(table_rows), width="stretch", hide_index=True)

        # Action Buttons Row (Download PDF, TXT, and Delete)
        st.markdown("<br>", unsafe_allow_html=True)
        c_btn1, c_btn2, c_del = st.columns([1.5, 1.2, 1.1])

        hist_res = dict(res)
        hist_res.setdefault("disease", disease)
        hist_res.setdefault("disease_name", name)
        hist_res.setdefault("user_inputs", inputs)
        hist_res.setdefault("created_at", r.get("created_at"))

        pdf_bytes = generate_diagnostic_report_pdf(hist_res)
        txt_content = generate_diagnostic_report_text(hist_res)
        run_tag = str(r.get("id", r.get("created_at", "run")))[:8]
        run_id = r.get("id") or r.get("created_at")

        with c_btn1:
            st.download_button(
                label="📥 Download Report (PDF)",
                data=pdf_bytes,
                file_name=f"{disease}_screening_report_{run_tag}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
                key=f"pdf_btn_{run_id}",
                help="Download official publication-grade clinical diagnostic screening report in PDF format.",
            )

        with c_btn2:
            st.download_button(
                label="📄 Text Summary (.txt)",
                data=txt_content,
                file_name=f"{disease}_screening_report_{run_tag}.txt",
                mime="text/plain",
                use_container_width=True,
                key=f"txt_btn_{run_id}",
                help="Download plain-text diagnostic summary report.",
            )

        with c_del:
            with st.popover("🗑️ Delete", help="Delete this individual screening record"):
                st.markdown(f"**Delete {name} record?**")
                st.caption(f"Screened on {created_str}. This cannot be undone.")
                if st.button("Confirm Delete", key=f"del_confirm_{run_id}", type="primary", use_container_width=True):
                    delete_run(run_id)
                    st.toast("Record deleted.", icon="🗑️")
                    st.rerun()
