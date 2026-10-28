"""
Preprocessing pipeline for Breast Cancer (WDBC) dataset and inference.
"""
import pandas as pd
import numpy as np

BREAST_CANCER_FEATURE_ORDER = [
    "mean radius", "mean texture", "mean perimeter", "mean area",
    "mean smoothness", "mean compactness", "mean concavity",
    "mean concave points", "mean symmetry", "mean fractal dimension"
]

def clean_breast_cancer_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts core 10 diagnostic mean features and standardizes target (1 = Malignant, 0 = Benign).
    """
    df = df.copy()

    # If raw sklearn target: 0 is malignant, 1 is benign
    # We map 1 -> Malignant, 0 -> Benign
    if "target" in df.columns:
        # Check if values are 0/1
        if set(df["target"].unique()).issubset({0, 1}):
            # sklearn target has 0 as malignant, so flip: 1 - x
            df["target"] = 1 - df["target"]
        elif "diagnosis" in df.columns or df["target"].dtype == object:
            df["target"] = df["target"].astype(str).str.upper().apply(lambda x: 1 if "M" in x or "MALIGNANT" in x else 0)

    # Select only the 10 core mean features + target
    cols_to_keep = [c for c in BREAST_CANCER_FEATURE_ORDER if c in df.columns]
    if "target" in df.columns:
        cols_to_keep.append("target")

    df = df[cols_to_keep].dropna()
    return df

def format_breast_cancer_input(user_input: dict) -> pd.DataFrame:
    """
    Transforms user input dictionary from UI into a single-row DataFrame
    matching the 10 diagnostic features for model pipeline inference.
    """
    row = {
        "mean radius": float(user_input.get("mean_radius", user_input.get("mean radius", 14.1))),
        "mean texture": float(user_input.get("mean_texture", user_input.get("mean texture", 19.3))),
        "mean perimeter": float(user_input.get("mean_perimeter", user_input.get("mean perimeter", 92.0))),
        "mean area": float(user_input.get("mean_area", user_input.get("mean area", 654.0))),
        "mean smoothness": float(user_input.get("mean_smoothness", user_input.get("mean smoothness", 0.096))),
        "mean compactness": float(user_input.get("mean_compactness", user_input.get("mean compactness", 0.104))),
        "mean concavity": float(user_input.get("mean_concavity", user_input.get("mean concavity", 0.088))),
        "mean concave points": float(user_input.get("mean_concave_points", user_input.get("mean concave points", 0.048))),
        "mean symmetry": float(user_input.get("mean_symmetry", user_input.get("mean symmetry", 0.181))),
        "mean fractal dimension": float(user_input.get("mean_fractal_dimension", user_input.get("mean fractal dimension", 0.062)))
    }
    return pd.DataFrame([row], columns=BREAST_CANCER_FEATURE_ORDER)
