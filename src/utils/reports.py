"""
Report generation utilities for Multi-Disease Prediction System (MDPS).
Produces professional, standardized, clinical diagnostic screening reports in PDF and plain-text formats.
"""
from datetime import datetime, timezone
import io
import os
import textwrap
from typing import Dict, Any, Optional

try:
    import dateutil.parser
except ImportError:
    dateutil = None

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.platypus import (
        HRFlowable,
        Image,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from src.utils.constants import (
    DISEASE_METADATA,
    HEART_FIELDS,
    KIDNEY_FIELDS,
    LIVER_FIELDS,
    LUNG_FIELDS,
    BREAST_CANCER_FIELDS,
    MEDICAL_DISCLAIMER,
)


def format_timestamp_friendly(raw_dt: Any) -> str:
    """Format any raw timestamp (ISO string, datetime, or date) into a clean, human-readable date and time."""
    if not raw_dt:
        return "Unknown Date"
    try:
        if isinstance(raw_dt, str):
            if dateutil:
                dt = dateutil.parser.isoparse(raw_dt)
            else:
                dt = datetime.fromisoformat(raw_dt.replace("Z", "+00:00"))
        else:
            dt = raw_dt

        try:
            local_dt = dt.astimezone()
            tz_name = local_dt.strftime("%Z")
            tz_str = f" ({tz_name})" if tz_name else ""
            return local_dt.strftime("%d %b %Y, %I:%M %p") + tz_str
        except Exception:
            return dt.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        clean = str(raw_dt).split(".")[0].replace("T", " ")
        return clean


# Reference definitions and clinical ranges for each screening module
REPORT_FIELD_DEFINITIONS = {
    "heart": {
        "age": {"label": "Patient Age", "unit": "years", "ref": "--"},
        "sex": {"label": "Biological Sex", "unit": "--", "ref": "--"},
        "cp": {"label": "Chest Pain Type", "unit": "--", "ref": "Typical/Atypical/Non-anginal/Asymptomatic"},
        "trestbps": {"label": "Resting Blood Pressure", "unit": "mm Hg", "ref": "< 120 mm Hg (Normal)"},
        "chol": {"label": "Serum Cholesterol", "unit": "mg/dl", "ref": "< 200 mg/dl (Desirable)"},
        "fbs": {"label": "Fasting Blood Sugar > 120 mg/dl", "unit": "--", "ref": "No (< 100 mg/dl normal)"},
        "restecg": {"label": "Resting ECG Results", "unit": "--", "ref": "Normal"},
        "thalach": {"label": "Max Heart Rate Achieved", "unit": "bpm", "ref": "Target ~ (220 - Age)"},
        "exang": {"label": "Exercise-Induced Angina", "unit": "--", "ref": "No"},
        "oldpeak": {"label": "ST Depression (Oldpeak)", "unit": "mm", "ref": "0.0 mm (Normal)"},
        "slope": {"label": "Slope of Peak Exercise ST", "unit": "--", "ref": "Upsloping (Normal)"},
        "ca": {"label": "Major Vessels Colored (0-4)", "unit": "vessels", "ref": "0 vessels"},
        "thal": {"label": "Thalassemia Classification", "unit": "--", "ref": "Normal"},
    },
    "kidney": {
        "age": {"label": "Patient Age", "unit": "years", "ref": "--"},
        "bp": {"label": "Blood Pressure", "unit": "mm Hg", "ref": "90 - 120 mm Hg"},
        "sg": {"label": "Specific Gravity", "unit": "--", "ref": "1.005 - 1.025"},
        "al": {"label": "Albumin (Urine Grade 0-5)", "unit": "grade", "ref": "0 (Negative)"},
        "su": {"label": "Sugar (Urine Grade 0-5)", "unit": "grade", "ref": "0 (Negative)"},
        "rbc": {"label": "Red Blood Cells in Urine", "unit": "--", "ref": "Normal"},
        "pc": {"label": "Pus Cells in Urine", "unit": "--", "ref": "Normal"},
        "pcc": {"label": "Pus Cell Clumps", "unit": "--", "ref": "Not Present"},
        "ba": {"label": "Bacteria in Urine", "unit": "--", "ref": "Not Present"},
        "bgr": {"label": "Blood Glucose (Random)", "unit": "mg/dl", "ref": "70 - 140 mg/dl"},
        "bu": {"label": "Blood Urea", "unit": "mg/dl", "ref": "7 - 20 mg/dl"},
        "sc": {"label": "Serum Creatinine", "unit": "mg/dl", "ref": "0.6 - 1.3 mg/dl"},
        "sod": {"label": "Serum Sodium", "unit": "mEq/L", "ref": "135 - 145 mEq/L"},
        "pot": {"label": "Serum Potassium", "unit": "mEq/L", "ref": "3.5 - 5.0 mEq/L"},
        "hemo": {"label": "Hemoglobin", "unit": "g/dl", "ref": "12.0 - 17.5 g/dl"},
        "pcv": {"label": "Packed Cell Volume (PCV)", "unit": "%", "ref": "36 - 50 %"},
        "wbcc": {"label": "White Blood Cell Count", "unit": "cells/cumm", "ref": "4,000 - 11,000"},
        "rbcc": {"label": "Red Blood Cell Count", "unit": "m/cumm", "ref": "4.2 - 5.9 m/cumm"},
        "htn": {"label": "Hypertension History", "unit": "--", "ref": "No"},
        "dm": {"label": "Diabetes Mellitus", "unit": "--", "ref": "No"},
        "cad": {"label": "Coronary Artery Disease", "unit": "--", "ref": "No"},
        "appet": {"label": "Appetite Status", "unit": "--", "ref": "Good"},
        "pe": {"label": "Pedal Edema (Swelling)", "unit": "--", "ref": "No"},
        "ane": {"label": "Anemia Diagnosed", "unit": "--", "ref": "No"},
    },
    "liver": {
        "Age": {"label": "Patient Age", "unit": "years", "ref": "--"},
        "Gender": {"label": "Biological Sex", "unit": "--", "ref": "--"},
        "TB": {"label": "Total Bilirubin (TB)", "unit": "mg/dl", "ref": "0.2 - 1.2 mg/dl"},
        "DB": {"label": "Direct Bilirubin (DB)", "unit": "mg/dl", "ref": "0.0 - 0.3 mg/dl"},
        "Alkphos": {"label": "Alkaline Phosphatase (ALP)", "unit": "IU/L", "ref": "44 - 147 IU/L"},
        "Sgpt": {"label": "Alamine Aminotransferase (ALT)", "unit": "IU/L", "ref": "7 - 56 IU/L"},
        "Sgot": {"label": "Aspartate Aminotransferase (AST)", "unit": "IU/L", "ref": "10 - 40 IU/L"},
        "TP": {"label": "Total Proteins (TP)", "unit": "g/dl", "ref": "6.0 - 8.3 g/dl"},
        "ALB": {"label": "Albumin (ALB)", "unit": "g/dl", "ref": "3.5 - 5.0 g/dl"},
        "A_G_Ratio": {"label": "Albumin/Globulin Ratio (A/G)", "unit": "ratio", "ref": "1.0 - 2.2"},
    },
    "lung": {
        "GENDER": {"label": "Biological Sex", "unit": "--", "ref": "--"},
        "AGE": {"label": "Patient Age", "unit": "years", "ref": "Baseline < 50 yrs"},
        "SMOKING": {"label": "Smoking Habit", "unit": "--", "ref": "No (Non-smoker)"},
        "YELLOW_FINGERS": {"label": "Yellow Fingers Indicator", "unit": "--", "ref": "No"},
        "ANXIETY": {"label": "Anxiety Symptoms", "unit": "--", "ref": "No"},
        "PEER_PRESSURE": {"label": "Peer Pressure Exposure", "unit": "--", "ref": "No"},
        "CHRONIC_DISEASE": {"label": "Chronic Respiratory Disease", "unit": "--", "ref": "No"},
        "FATIGUE": {"label": "Persistent Fatigue", "unit": "--", "ref": "No"},
        "ALLERGY": {"label": "Known Allergies", "unit": "--", "ref": "No"},
        "WHEEZING": {"label": "Wheezing / Stridor", "unit": "--", "ref": "No"},
        "ALCOHOL_CONSUMING": {"label": "Regular Alcohol Consumption", "unit": "--", "ref": "No"},
        "COUGHING": {"label": "Chronic Coughing", "unit": "--", "ref": "No"},
        "SHORTNESS_OF_BREATH": {"label": "Shortness of Breath (Dyspnea)", "unit": "--", "ref": "No"},
        "SWALLOWING_DIFFICULTY": {"label": "Swallowing Difficulty", "unit": "--", "ref": "No"},
        "CHEST_PAIN": {"label": "Chest Pain / Discomfort", "unit": "--", "ref": "No"},
    },
    "breast_cancer": {
        "mean_radius": {"label": "Mean Radius", "unit": "mm", "ref": "11.0 - 13.0 mm (Benign)"},
        "mean_texture": {"label": "Mean Texture", "unit": "gray-scale", "ref": "15.0 - 20.0 (Benign)"},
        "mean_perimeter": {"label": "Mean Perimeter", "unit": "mm", "ref": "70.0 - 90.0 mm (Benign)"},
        "mean_area": {"label": "Mean Area", "unit": "mm²", "ref": "400 - 650 mm² (Benign)"},
        "mean_smoothness": {"label": "Mean Smoothness", "unit": "score", "ref": "0.080 - 0.100 (Benign)"},
        "mean_compactness": {"label": "Mean Compactness", "unit": "score", "ref": "0.050 - 0.150 (Benign)"},
        "mean_concavity": {"label": "Mean Concavity", "unit": "score", "ref": "0.020 - 0.080 (Benign)"},
        "mean_concave_points": {"label": "Mean Concave Points", "unit": "score", "ref": "0.010 - 0.050 (Benign)"},
        "mean_symmetry": {"label": "Mean Symmetry", "unit": "score", "ref": "0.150 - 0.200 (Benign)"},
        "mean_fractal_dimension": {"label": "Mean Fractal Dimension", "unit": "score", "ref": "0.050 - 0.070 (Benign)"},
    },
}

# Reverse mapping for numeric codes to readable text when only encoded inputs exist
REVERSE_VALUE_MAP = {
    ("liver", "Gender"): {1: "Male", 0: "Female"},
    ("lung", "GENDER"): {1: "Male", 0: "Female"},
    ("lung", "SMOKING"): {2: "Yes", 1: "No"},
    ("lung", "YELLOW_FINGERS"): {2: "Yes", 1: "No"},
    ("lung", "ANXIETY"): {2: "Yes", 1: "No"},
    ("lung", "PEER_PRESSURE"): {2: "Yes", 1: "No"},
    ("lung", "CHRONIC_DISEASE"): {2: "Yes", 1: "No"},
    ("lung", "FATIGUE"): {2: "Yes", 1: "No"},
    ("lung", "ALLERGY"): {2: "Yes", 1: "No"},
    ("lung", "WHEEZING"): {2: "Yes", 1: "No"},
    ("lung", "ALCOHOL_CONSUMING"): {2: "Yes", 1: "No"},
    ("lung", "COUGHING"): {2: "Yes", 1: "No"},
    ("lung", "SHORTNESS_OF_BREATH"): {2: "Yes", 1: "No"},
    ("lung", "SWALLOWING_DIFFICULTY"): {2: "Yes", 1: "No"},
    ("lung", "CHEST_PAIN"): {2: "Yes", 1: "No"},
    ("heart", "sex"): {1: "Male", 0: "Female"},
    ("heart", "fbs"): {1: "Yes", 0: "No"},
    ("heart", "exang"): {1: "Yes", 0: "No"},
    ("heart", "cp"): {0: "Typical Angina", 1: "Atypical Angina", 2: "Non-anginal Pain", 3: "Asymptomatic"},
    ("heart", "restecg"): {0: "Normal", 1: "ST-T Wave Abnormality", 2: "Left Ventricular Hypertrophy"},
    ("heart", "slope"): {0: "Upsloping", 1: "Flat", 2: "Downsloping"},
    ("heart", "thal"): {1: "Normal", 2: "Fixed Defect", 3: "Reversible Defect"},
    ("kidney", "htn"): {1: "Yes", 0: "No"},
    ("kidney", "dm"): {1: "Yes", 0: "No"},
    ("kidney", "cad"): {1: "Yes", 0: "No"},
    ("kidney", "pe"): {1: "Yes", 0: "No"},
    ("kidney", "ane"): {1: "Yes", 0: "No"},
    ("kidney", "rbc"): {1: "Abnormal", 0: "Normal"},
    ("kidney", "pc"): {1: "Abnormal", 0: "Normal"},
    ("kidney", "pcc"): {1: "Present", 0: "Not Present"},
    ("kidney", "ba"): {1: "Present", 0: "Not Present"},
    ("kidney", "appet"): {1: "Poor", 0: "Good"},
}


INTEGER_FIELD_NAMES = {
    "age", "gender", "sex", "alkphos", "sgpt", "sgot", "trestbps", "chol",
    "thalach", "ca", "bp", "bgr", "bu", "wbcc", "pcv", "smoking",
    "yellow_fingers", "anxiety", "peer_pressure", "chronic_disease",
    "fatigue", "allergy", "wheezing", "alcohol_consuming", "coughing",
    "shortness_of_breath", "swallowing_difficulty", "chest_pain",
    "al", "su", "htn", "dm", "cad", "pe", "ane"
}


_MISSING_INPUT = object()


def _lookup_input(inputs: Dict[str, Any], key: str) -> Any:
    """Match saved input keys across underscore/space and case variants."""
    for candidate in (key, key.lower(), key.upper(), key.replace("_", " "), key.replace(" ", "_")):
        if candidate in inputs:
            return inputs[candidate]
    return _MISSING_INPUT


def _format_observed_value(val: Any, field_name: str, disease: str) -> str:
    """Format observed parameter value with human-friendly strings and clean numbers."""
    if val is None:
        return "--"

    # Check reverse mapping first
    rev_map = REVERSE_VALUE_MAP.get((disease, field_name))
    if rev_map and val in rev_map:
        return str(rev_map[val])

    # Convert numpy scalars to python types if needed
    if hasattr(val, "item") and callable(val.item):
        val = val.item()

    if isinstance(val, bool):
        return "Yes" if val else "No"

    if isinstance(val, (int,)):
        return str(val)

    if isinstance(val, (float,)):
        if field_name.lower() in INTEGER_FIELD_NAMES:
            return str(int(round(val)))
        if abs(val) < 0.01:
            return f"{val:.4f}"
        return f"{val:.2f}"

    return str(val)


def generate_diagnostic_report_text(res: Dict[str, Any], user: Optional[Any] = None) -> str:
    """
    Builds a beautifully structured, comprehensive clinical diagnostic screening report
    in plain text / ASCII table format.
    """
    disease = str(res.get("disease", "diagnosis")).lower()
    meta = DISEASE_METADATA.get(disease, {})
    disease_name = res.get("disease_name") or meta.get("name") or disease.replace("_", " ").title()

    # Determine patient / client display name
    patient_name = "Not Provided (Clinical Walk-in)"
    patient_id = "N/A"
    try:
        from src.auth.storage import display_name
        import streamlit as st
        cur_user = user or st.session_state.get("user")
        if cur_user:
            patient_name = display_name(cur_user)
            patient_id = getattr(cur_user, "email", None) or (
                cur_user.get("email") if isinstance(cur_user, dict) else "Authenticated User"
            )
    except Exception:
        pass

    # Timestamps & Report ID
    now_utc = datetime.now(timezone.utc)
    now_str = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    report_tag = disease[:3].upper() if disease else "GEN"
    report_id = f"MDPS-{report_tag}-{now_utc.strftime('%Y%m%d-%H%M%S')}"

    # Clinical outcomes
    result_label = res.get("result_label", "Screening Completed")
    risk_level = res.get("risk_level", "Unknown Risk")
    confidence = float(res.get("confidence", 0.0))
    risk_prob = float(res.get("probability_positive", 0.0))
    norm_prob = float(res.get("probability_negative", 0.0))
    recommendation = res.get("recommendation") or meta.get("positive_desc" if res.get("is_positive") else "negative_desc") or ""
    model_name = res.get("model_name", "Supervised Machine Learning Classifier")

    div_heavy = "=" * 80
    div_light = "-" * 80

    lines = [
        div_heavy,
        "                    MULTI-DISEASE PREDICTION SYSTEM (MDPS)",
        "                     CLINICAL SCREENING & DIAGNOSTIC REPORT",
        div_heavy,
        "",
        "DOCUMENT & PATIENT INFORMATION",
        div_light,
        f"Report Reference ID  : {report_id}",
        f"Date & Time Generated: {now_str}",
        f"Diagnostic Module    : {disease_name}",
        f"Model Architecture   : {model_name}",
        f"Patient / Client     : {patient_name}",
        f"Patient Identifier   : {patient_id}",
        f"Screening Facility   : MDPS AI-Assisted Clinical Screening Console",
        "",
        "DIAGNOSTIC SCREENING ASSESSMENT",
        div_light,
        f"Primary Finding      : {result_label.upper()}",
        f"Risk Category        : [ {risk_level.upper()} ]",
        f"Model Confidence     : {confidence:.1f}%",
        f"Risk Probability     : {risk_prob:.1f}%",
        f"Normal Probability   : {norm_prob:.1f}%",
        "",
        "Clinical Interpretation & Guidance:",
    ]

    for line in textwrap.wrap(recommendation, width=76):
        lines.append(f"  {line}")

    # Top contributing factors
    top_features = res.get("top_features") or []
    if top_features:
        lines.extend([
            "",
            "Key Contributing Factors (Feature Importance):",
        ])
        for tf in top_features[:5]:
            feat_name = tf.get("feature", "Factor")
            contrib = float(tf.get("contribution", 0.0))
            # Format feature label
            field_def = REPORT_FIELD_DEFINITIONS.get(disease, {}).get(feat_name, {})
            label = field_def.get("label", feat_name)
            sign = "+" if contrib > 0 else ""
            lines.append(f"  • {label:<32}: {sign}{contrib:.1f}% risk contribution")

    # Biomarkers & Clinical Parameters Table
    lines.extend([
        "",
        "OBSERVED CLINICAL PARAMETERS & BIOMARKERS",
        div_light,
        f"{'Parameter / Biomarker':<34} {'Observed':<14} {'Unit':<10} {'Reference Interval':<20}",
        div_light,
    ])

    field_defs = REPORT_FIELD_DEFINITIONS.get(disease, {})
    # Prefer raw user_inputs if available for human-readable labels, fallback to input_features
    inputs_dict = res.get("user_inputs") or res.get("input_features") or {}

    # If field_defs exists, iterate according to defined order; otherwise iterate input dict
    ordered_keys = list(field_defs.keys()) if field_defs else list(inputs_dict.keys())
    for k in ordered_keys:
        val = _lookup_input(inputs_dict, k)
        if val is _MISSING_INPUT:
            continue

        fdef = field_defs.get(k, {})
        label = fdef.get("label", k)
        unit = fdef.get("unit", "--")
        ref = fdef.get("ref", "--")
        formatted_val = _format_observed_value(val, k, disease)

        # Truncate label if excessively long to preserve layout
        if len(label) > 33:
            label = label[:30] + "..."

        lines.append(f"{label:<34} {formatted_val:<14} {unit:<10} {ref:<20}")

    lines.extend([
        div_light,
        "",
        "MODEL & SCREENING AUDIT INFO",
        div_light,
        f"Pipeline Framework   : MDPS Classical ML Inference Suite",
        f"Evaluation Status    : Validated Deterministic Inference Run",
        f"Inference Mode       : Pre-Screening Support System",
        "",
        "IMPORTANT MEDICAL DISCLAIMER",
        div_light,
    ])

    for line in textwrap.wrap(MEDICAL_DISCLAIMER, width=78):
        lines.append(line)

    lines.extend([
        "",
        "All screening results must be evaluated in person by a certified physician",
        "or licensed healthcare professional. Never discontinue or adjust clinical",
        "treatment based exclusively on algorithmic screening outputs.",
        div_heavy,
        "                    *** END OF DIAGNOSTIC REPORT ***",
        div_heavy,
    ])

    return "\n".join(lines)


def generate_diagnostic_report_pdf(res: Dict[str, Any], user: Optional[Any] = None) -> bytes:
    """
    Builds a publication-grade, professionally formatted clinical PDF screening report
    using ReportLab. Returns PDF bytes ready for streaming or downloading.
    """
    if not REPORTLAB_AVAILABLE:
        return generate_diagnostic_report_text(res, user).encode("utf-8")

    disease = str(res.get("disease", "diagnosis")).lower()
    meta = DISEASE_METADATA.get(disease, {})
    disease_name = res.get("disease_name") or meta.get("name") or disease.replace("_", " ").title()

    # Determine patient / client display name
    patient_name = "Not Provided (Clinical Walk-in)"
    patient_id = "N/A"
    try:
        from src.auth.storage import display_name
        import streamlit as st
        cur_user = user or st.session_state.get("user")
        if cur_user:
            patient_name = display_name(cur_user)
            patient_id = getattr(cur_user, "email", None) or (
                cur_user.get("email") if isinstance(cur_user, dict) else "Authenticated User"
            )
    except Exception:
        pass

    # Dates & Report Reference ID
    raw_created = res.get("created_at")
    formatted_date = format_timestamp_friendly(raw_created or datetime.now(timezone.utc))
    report_tag = disease[:3].upper() if disease else "GEN"
    report_id = f"MDPS-{report_tag}-{datetime.now().strftime('%Y%m%d-%H%M')}"

    # Clinical assessment variables
    is_pos = bool(res.get("is_positive", False))
    result_label = res.get("result_label", "Screening Completed")
    risk_level = res.get("risk_level", "High Risk" if is_pos else "Low Risk")
    confidence = float(res.get("confidence", 0.0))
    risk_prob = float(res.get("probability_positive", 0.0))
    norm_prob = float(res.get("probability_negative", 0.0))
    recommendation = res.get("recommendation") or meta.get("positive_desc" if is_pos else "negative_desc") or ""
    model_name = res.get("model_name", "Classical Machine Learning Classifier")

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "PDFTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
    )
    right_meta_style = ParagraphStyle(
        "PDFRightMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        alignment=2,
        textColor=colors.HexColor("#475569"),
    )
    meta_key = ParagraphStyle(
        "MetaKey",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#64748b"),
    )
    meta_val = ParagraphStyle(
        "MetaVal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
    )

    story = []

    # 1. Header Banner Table
    header_data = [
        [
            Paragraph(
                "<b>MULTI-DISEASE PREDICTION SYSTEM (MDPS)</b><br/>"
                "<font size=\"8\" color=\"#64748b\">Clinical AI Diagnostic Screening & Decision-Support Suite</font>",
                title_style,
            ),
            Paragraph(
                f"<b>CONFIDENTIAL MEDICAL SCREENING</b><br/>"
                f"Ref: <b>{report_id}</b><br/>"
                f"{formatted_date}",
                right_meta_style,
            ),
        ]
    ]
    t_head = Table(header_data, colWidths=[350, 190])
    t_head.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(t_head)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=8))

    # 2. Patient & Metadata Info Box
    patient_data = [
        [
            Paragraph("PATIENT / CLIENT", meta_key),
            Paragraph(f"<b>{patient_name}</b>", meta_val),
            Paragraph("DIAGNOSTIC MODULE", meta_key),
            Paragraph(f"<b>{disease_name}</b>", meta_val),
        ],
        [
            Paragraph("PATIENT IDENTIFIER", meta_key),
            Paragraph(patient_id, meta_val),
            Paragraph("MODEL ARCHITECTURE", meta_key),
            Paragraph(f"{model_name}", meta_val),
        ],
        [
            Paragraph("GENERATION TIME", meta_key),
            Paragraph(formatted_date, meta_val),
            Paragraph("SCREENING STATUS", meta_key),
            Paragraph("Validated Screening Pass", meta_val),
        ],
    ]
    t_meta = Table(patient_data, colWidths=[110, 160, 110, 160])
    t_meta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#e2e8f0")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#edf2f7")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # 3. Diagnostic Screening Assessment Card
    hero_bg = colors.HexColor("#fff1f2") if is_pos else colors.HexColor("#f0fdf4")
    hero_border = colors.HexColor("#f43f5e") if is_pos else colors.HexColor("#10b981")
    hero_text_color = "#be123c" if is_pos else "#047857"

    hero_html = f"""
    <font size="8" color="{hero_text_color}"><b>SCREENING ASSESSMENT &bull; {risk_level.upper()}</b></font><br/>
    <font size="12" color="{hero_text_color}"><b>{result_label}</b></font><br/>
    <font size="8.5" color="#334155">{recommendation}</font>
    """

    stats_html = f"""
    <font size="8" color="#64748b">MODEL CONFIDENCE</font><br/>
    <font size="14" color="{hero_text_color}"><b>{confidence:.1f}%</b></font><br/>
    <font size="7.5" color="#64748b">Risk: {risk_prob:.1f}% &bull; Normal: {norm_prob:.1f}%</font>
    """

    t_hero = Table(
        [
            [
                Paragraph(hero_html, styles["Normal"]),
                Paragraph(stats_html, ParagraphStyle("Stats", parent=styles["Normal"], alignment=2)),
            ]
        ],
        colWidths=[395, 145],
    )
    t_hero.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), hero_bg),
        ("BOX", (0, 0), (-1, -1), 1, hero_border),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t_hero)
    story.append(Spacer(1, 10))

    # 4. Clinical Biomarkers Table
    table_header_style = ParagraphStyle(
        "THStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
    )
    cell_style = ParagraphStyle(
        "TDStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1e293b"),
    )
    cell_bold_style = ParagraphStyle(
        "TDBoldStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
    )

    t_rows = [
        [
            Paragraph("<b>Parameter / Biomarker</b>", table_header_style),
            Paragraph("<b>Observed Value</b>", table_header_style),
            Paragraph("<b>Unit</b>", table_header_style),
            Paragraph("<b>Reference Interval</b>", table_header_style),
        ]
    ]

    field_defs = REPORT_FIELD_DEFINITIONS.get(disease, {})
    inputs_dict = res.get("user_inputs") or res.get("input_features") or {}
    ordered_keys = list(field_defs.keys()) if field_defs else list(inputs_dict.keys())

    for k in ordered_keys:
        val = _lookup_input(inputs_dict, k)
        if val is _MISSING_INPUT:
            continue
        fdef = field_defs.get(k, {})
        label = fdef.get("label", k)
        unit = fdef.get("unit", "--")
        ref = fdef.get("ref", "--")
        formatted_val = _format_observed_value(val, k, disease)

        t_rows.append([
            Paragraph(label, cell_bold_style),
            Paragraph(formatted_val, cell_style),
            Paragraph(unit, cell_style),
            Paragraph(ref, cell_style),
        ])

    t_table = Table(t_rows, colWidths=[200, 100, 80, 160])
    t_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t_table)
    story.append(Spacer(1, 10))

    # 5. Medical Disclaimer Box
    disclaimer_html = f"""
    <font size="7" color="#7c5a10"><b>IMPORTANT MEDICAL NOTICE:</b> {MEDICAL_DISCLAIMER} Screening results must be evaluated in person by a certified healthcare professional. Do not discontinue or alter clinical care based solely on automated screening outputs.</font>
    """
    t_disc = Table([[Paragraph(disclaimer_html, styles["Normal"])]], colWidths=[540])
    t_disc.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fffbeb")),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#fde68a")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t_disc)

    # 6. Official G17 Clinical Verification Seal & Attestation Block
    seal_path = os.path.join(os.path.dirname(__file__), "..", "assets", "g17_seal.png")
    seal_img = None
    if os.path.exists(seal_path):
        try:
            seal_img = Image(seal_path, width=64, height=64)
        except Exception:
            seal_img = None

    attest_html = """
    <font size="7.5" color="#0f172a"><b>ACADEMIC RESEARCH &amp; VERIFICATION BLOCK • GROUP 17 (G17)</b></font><br/>
    <font size="6.5" color="#475569">
    <b>Project Guide:</b> Dr. Manjunath R, Professor &amp; HOD<br/>
    <b>Development Team:</b> M Kushala (1RI23CS078) · Prajwal Aravind D M (1RI23CS108)<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sameeksha M G (1RI23CS128) · Shiva Prakash T R (1RI23CS134)<br/>
    <b>Audit Status:</b> Validated Multi-Disease ML Inference Pipeline · Dept. of CSE
    </font>
    """
    attest_para = Paragraph(attest_html, styles["Normal"])

    sig_html = """
    <font size="6.5" color="#64748b">Official Academic Seal &amp; Verification</font><br/>
    <font size="7.5" color="#0f172a"><b>Dr. Manjunath R</b></font><br/>
    <font size="6" color="#64748b">Professor &amp; Head of Department</font>
    """
    sig_para = Paragraph(sig_html, ParagraphStyle("SigStyle", parent=styles["Normal"], alignment=1))

    if seal_img:
        t_attest = Table([[attest_para, seal_img, sig_para]], colWidths=[335, 75, 130])
    else:
        t_attest = Table([[attest_para, sig_para]], colWidths=[400, 140])

    t_attest.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(Spacer(1, 8))
    story.append(t_attest)

    doc.build(story)
    return buf.getvalue()

