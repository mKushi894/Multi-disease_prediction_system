"""
Preprocessing pipeline for Lung Cancer / Lung Disease dataset and inference.
"""
import pandas as pd
import numpy as np

LUNG_FEATURE_ORDER = [
    "GENDER", "AGE", "SMOKING", "YELLOW_FINGERS", "ANXIETY", "PEER_PRESSURE",
    "CHRONIC_DISEASE", "FATIGUE", "ALLERGY", "WHEEZING", "ALCOHOL_CONSUMING",
    "COUGHING", "SHORTNESS_OF_BREATH", "SWALLOWING_DIFFICULTY", "CHEST_PAIN"
]

GENDER_MAP = {"Male": 1, "Female": 0, "M": 1, "F": 0, "m": 1, "f": 0}
# Survey data uses 1 for No, 2 for Yes
SURVEY_MAP = {"No": 1, "Yes": 2, "no": 1, "yes": 2, 1: 1, 2: 2, 0: 1}

def clean_lung_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw Lung Cancer dataset, normalizes column names and maps binary indicators.
    """
    df = df.copy()

    # Standardize column names (strip trailing spaces, replace spaces with underscores)
    cleaned_cols = {c: c.strip().replace(" ", "_") for c in df.columns}
    df = df.rename(columns=cleaned_cols)

    # Encode Gender
    if "GENDER" in df.columns:
        df["GENDER"] = df["GENDER"].astype(str).str.strip().map(GENDER_MAP).fillna(1).astype(int)

    # Encode Target
    if "LUNG_CANCER" in df.columns:
        df["target"] = df["LUNG_CANCER"].astype(str).str.strip().str.upper().apply(lambda x: 1 if x == "YES" else 0)
        df = df.drop(columns=["LUNG_CANCER"])

    df = df.dropna()
    # Deduplicate to prevent train/test data leakage across identical survey responses
    df = df.drop_duplicates()
    return df

def format_lung_input(user_input: dict) -> pd.DataFrame:
    """
    Transforms user input dictionary from UI into a single-row DataFrame
    for the trained Lung model pipeline.
    """
    row = {
        "GENDER": GENDER_MAP.get(user_input["GENDER"], 1),
        "AGE": float(user_input["AGE"]),
        "SMOKING": SURVEY_MAP.get(user_input["SMOKING"], 1),
        "YELLOW_FINGERS": SURVEY_MAP.get(user_input["YELLOW_FINGERS"], 1),
        "ANXIETY": SURVEY_MAP.get(user_input["ANXIETY"], 1),
        "PEER_PRESSURE": SURVEY_MAP.get(user_input["PEER_PRESSURE"], 1),
        "CHRONIC_DISEASE": SURVEY_MAP.get(user_input["CHRONIC_DISEASE"], 1),
        "FATIGUE": SURVEY_MAP.get(user_input["FATIGUE"], 1),
        "ALLERGY": SURVEY_MAP.get(user_input["ALLERGY"], 1),
        "WHEEZING": SURVEY_MAP.get(user_input["WHEEZING"], 1),
        "ALCOHOL_CONSUMING": SURVEY_MAP.get(user_input["ALCOHOL_CONSUMING"], 1),
        "COUGHING": SURVEY_MAP.get(user_input["COUGHING"], 1),
        "SHORTNESS_OF_BREATH": SURVEY_MAP.get(user_input["SHORTNESS_OF_BREATH"], 1),
        "SWALLOWING_DIFFICULTY": SURVEY_MAP.get(user_input["SWALLOWING_DIFFICULTY"], 1),
        "CHEST_PAIN": SURVEY_MAP.get(user_input["CHEST_PAIN"], 1)
    }
    return pd.DataFrame([row], columns=LUNG_FEATURE_ORDER)
