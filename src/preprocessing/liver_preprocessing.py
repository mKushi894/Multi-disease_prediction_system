"""
Preprocessing pipeline for Indian Liver Patient Dataset (ILPD) and inference.
"""
import pandas as pd
import numpy as np

LIVER_FEATURE_ORDER = [
    "Age", "Gender", "TB", "DB", "Alkphos", "Sgpt", "Sgot", "TP", "ALB", "A_G_Ratio"
]

GENDER_MAP = {"Male": 1, "Female": 0, "male": 1, "female": 0}

def clean_liver_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw Liver dataset, handles missing values and standardizes column names.
    """
    df = df.copy()

    # Rename columns to standard names
    col_mapping = {
        "A/G Ratio": "A_G_Ratio",
        "Albumin_and_Globulin_Ratio": "A_G_Ratio",
        "Total_Bilirubin": "TB",
        "Direct_Bilirubin": "DB",
        "Alkaline_Phosphotase": "Alkphos",
        "Alamine_Aminotransferase": "Sgpt",
        "Aspartate_Aminotransferase": "Sgot",
        "Total_Protiens": "TP",
        "Albumin": "ALB",
        "Dataset": "Selector"
    }
    df = df.rename(columns=col_mapping)

    # Encode Gender
    if "Gender" in df.columns:
        df["Gender"] = df["Gender"].map(GENDER_MAP).fillna(1).astype(int)

    # Clean target: 1 = Patient (1), 2 = Non-Patient (0)
    if "Selector" in df.columns:
        df["target"] = df["Selector"].apply(lambda x: 1 if x == 1 else 0)
        df = df.drop(columns=["Selector"])

    # Impute missing values
    if "A_G_Ratio" in df.columns:
        df["A_G_Ratio"] = df["A_G_Ratio"].fillna(df["A_G_Ratio"].median())

    df = df.dropna()
    return df

def format_liver_input(user_input: dict) -> pd.DataFrame:
    """
    Transforms user input dictionary from UI into a single-row DataFrame
    for the trained Liver model pipeline.
    """
    row = {
        "Age": float(user_input["Age"]),
        "Gender": GENDER_MAP.get(user_input["Gender"], 1),
        "TB": float(user_input["TB"]),
        "DB": float(user_input["DB"]),
        "Alkphos": float(user_input["Alkphos"]),
        "Sgpt": float(user_input["Sgpt"]),
        "Sgot": float(user_input["Sgot"]),
        "TP": float(user_input["TP"]),
        "ALB": float(user_input["ALB"]),
        "A_G_Ratio": float(user_input["A_G_Ratio"])
    }
    return pd.DataFrame([row], columns=LIVER_FEATURE_ORDER)
