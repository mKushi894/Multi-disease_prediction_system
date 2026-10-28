"""
Preprocessing pipeline for Heart Disease dataset and inference.
"""
import pandas as pd
import numpy as np

HEART_FEATURE_ORDER = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]

SEX_MAP = {"Male": 1, "Female": 0}
CP_MAP = {"Typical Angina": 0, "Atypical Angina": 1, "Non-anginal Pain": 2, "Asymptomatic": 3}
FBS_MAP = {"Yes": 1, "No": 0}
RESTECG_MAP = {"Normal": 0, "ST-T Wave Abnormality": 1, "Left Ventricular Hypertrophy": 2}
EXANG_MAP = {"Yes": 1, "No": 0}
SLOPE_MAP = {"Upsloping": 0, "Flat": 1, "Downsloping": 2}
THAL_MAP = {"Normal": 1, "Fixed Defect": 2, "Reversible Defect": 3}

def format_heart_input(user_input: dict) -> pd.DataFrame:
    """
    Transforms raw user input dictionary from UI into a single-row DataFrame
    ready for model pipeline inference.
    """
    row = {
        "age": float(user_input["age"]),
        "sex": SEX_MAP.get(user_input["sex"], int(user_input["sex"]) if str(user_input["sex"]).isdigit() else 1),
        "cp": CP_MAP.get(user_input["cp"], int(user_input["cp"]) if str(user_input["cp"]).isdigit() else 0),
        "trestbps": float(user_input["trestbps"]),
        "chol": float(user_input["chol"]),
        "fbs": FBS_MAP.get(user_input["fbs"], int(user_input["fbs"]) if str(user_input["fbs"]).isdigit() else 0),
        "restecg": RESTECG_MAP.get(user_input["restecg"], int(user_input["restecg"]) if str(user_input["restecg"]).isdigit() else 0),
        "thalach": float(user_input["thalach"]),
        "exang": EXANG_MAP.get(user_input["exang"], int(user_input["exang"]) if str(user_input["exang"]).isdigit() else 0),
        "oldpeak": float(user_input["oldpeak"]),
        "slope": SLOPE_MAP.get(user_input["slope"], int(user_input["slope"]) if str(user_input["slope"]).isdigit() else 1),
        "ca": int(user_input["ca"]),
        "thal": THAL_MAP.get(user_input["thal"], int(user_input["thal"]) if str(user_input["thal"]).isdigit() else 1)
    }
    return pd.DataFrame([row], columns=HEART_FEATURE_ORDER)
