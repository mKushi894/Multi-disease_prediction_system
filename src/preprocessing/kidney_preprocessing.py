"""
Preprocessing pipeline for Chronic Kidney Disease (CKD) dataset and inference.
"""
import pandas as pd
import numpy as np

KIDNEY_FEATURE_ORDER = [
    "age", "bp", "sg", "al", "su", "rbc", "pc", "pcc", "ba",
    "bgr", "bu", "sc", "sod", "pot", "hemo", "pcv", "wbcc", "rbcc",
    "htn", "dm", "cad", "appet", "pe", "ane"
]

NORM_ABNORM_MAP = {"Normal": 0, "Abnormal": 1, "normal": 0, "abnormal": 1}
PRES_NOTPRES_MAP = {"Not Present": 0, "Present": 1, "notpresent": 0, "present": 1}
YES_NO_MAP = {"No": 0, "Yes": 1, "no": 0, "yes": 1}
APPET_MAP = {"Good": 0, "Poor": 1, "good": 0, "poor": 1}

def clean_ckd_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw CKD dataframe, standardizes string anomalies and missing values.
    """
    df = df.copy()

    # Clean target
    if "class" in df.columns:
        df["class"] = df["class"].astype(str).str.strip().str.lower()
        df["target"] = df["class"].apply(lambda x: 1 if "ckd" in x and "not" not in x else 0)
        df = df.drop(columns=["class"])

    # Clean string columns
    str_cols = ["rbc", "pc", "pcc", "ba", "htn", "dm", "cad", "appet", "pe", "ane"]
    for c in str_cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip().str.lower()
            df[c] = df[c].replace({"nan": np.nan, "none": np.nan, "?": np.nan, "\tno": "no", "\tyes": "yes", " yes": "yes"})

    # Map categoricals to numeric
    for c in ["rbc", "pc"]:
        if c in df.columns:
            df[c] = df[c].map(NORM_ABNORM_MAP)
    for c in ["pcc", "ba"]:
        if c in df.columns:
            df[c] = df[c].map(PRES_NOTPRES_MAP)
    for c in ["htn", "dm", "cad", "pe", "ane"]:
        if c in df.columns:
            df[c] = df[c].map(YES_NO_MAP)
    if "appet" in df.columns:
        df["appet"] = df["appet"].map(APPET_MAP)

    # Convert numeric columns
    for c in df.columns:
        if c != "target":
            df[c] = pd.to_numeric(df[c], errors="coerce")

    return df

def format_kidney_input(user_input: dict) -> pd.DataFrame:
    """
    Transforms user input dictionary from UI into a single-row DataFrame
    for the trained CKD model pipeline.
    """
    row = {
        "age": float(user_input["age"]),
        "bp": float(user_input["bp"]),
        "sg": float(user_input["sg"]),
        "al": float(user_input["al"]),
        "su": float(user_input["su"]),
        "rbc": NORM_ABNORM_MAP.get(user_input["rbc"], 0),
        "pc": NORM_ABNORM_MAP.get(user_input["pc"], 0),
        "pcc": PRES_NOTPRES_MAP.get(user_input["pcc"], 0),
        "ba": PRES_NOTPRES_MAP.get(user_input["ba"], 0),
        "bgr": float(user_input["bgr"]),
        "bu": float(user_input["bu"]),
        "sc": float(user_input["sc"]),
        "sod": float(user_input["sod"]),
        "pot": float(user_input["pot"]),
        "hemo": float(user_input["hemo"]),
        "pcv": float(user_input["pcv"]),
        "wbcc": float(user_input["wbcc"]),
        "rbcc": float(user_input["rbcc"]),
        "htn": YES_NO_MAP.get(user_input["htn"], 0),
        "dm": YES_NO_MAP.get(user_input["dm"], 0),
        "cad": YES_NO_MAP.get(user_input["cad"], 0),
        "appet": APPET_MAP.get(user_input["appet"], 0),
        "pe": YES_NO_MAP.get(user_input["pe"], 0),
        "ane": YES_NO_MAP.get(user_input["ane"], 0)
    }
    return pd.DataFrame([row], columns=KIDNEY_FEATURE_ORDER)
