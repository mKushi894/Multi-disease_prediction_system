"""
Comprehensive unit test suite to verify prediction pipelines and presets for all 5 disease modules.
"""
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.prediction.predict import predict_disease

TEST_CASES = {
    "heart": {
        "Low-Risk Sample": {
            "payload": {
                "age": 35, "sex": "Female", "cp": "Typical Angina", "trestbps": 118, "chol": 182,
                "fbs": "No", "restecg": "Normal", "thalach": 172, "exang": "No", "oldpeak": 0.0,
                "slope": "Upsloping", "ca": 0, "thal": "Normal"
            },
            "expected_risk": "Low Risk",
            "expected_positive": False
        },
        "High-Risk Sample": {
            "payload": {
                "age": 62, "sex": "Male", "cp": "Asymptomatic", "trestbps": 160, "chol": 290,
                "fbs": "Yes", "restecg": "Left Ventricular Hypertrophy", "thalach": 108, "exang": "Yes", "oldpeak": 3.2,
                "slope": "Downsloping", "ca": 2, "thal": "Reversible Defect"
            },
            "expected_risk": "High Risk",
            "expected_positive": True
        }
    },
    "kidney": {
        "Low-Risk Sample": {
            "payload": {
                "age": 42, "bp": 75, "sg": "1.025", "al": "0", "su": "0", "rbc": "Normal",
                "pc": "Normal", "pcc": "Not Present", "ba": "Not Present", "bgr": 95,
                "bu": 24.0, "sc": 0.8, "sod": 140.0, "pot": 4.1, "hemo": 15.6, "pcv": 46,
                "wbcc": 6800, "rbcc": 5.4, "htn": "No", "dm": "No", "cad": "No", "appet": "Good",
                "pe": "No", "ane": "No"
            },
            "expected_risk": "Low Risk",
            "expected_positive": False
        },
        "High-Risk Sample": {
            "payload": {
                "age": 64, "bp": 90, "sg": "1.010", "al": "3", "su": "2", "rbc": "Abnormal",
                "pc": "Abnormal", "pcc": "Present", "ba": "Present", "bgr": 240,
                "bu": 115.0, "sc": 4.2, "sod": 129.0, "pot": 5.6, "hemo": 8.6, "pcv": 27,
                "wbcc": 13500, "rbcc": 3.2, "htn": "Yes", "dm": "Yes", "cad": "Yes", "appet": "Poor",
                "pe": "Yes", "ane": "Yes"
            },
            "expected_risk": "High Risk",
            "expected_positive": True
        }
    },
    "liver": {
        "Low-Risk Sample": {
            "payload": {
                "Age": 28, "Gender": "Female", "TB": 0.7, "DB": 0.2, "Alkphos": 155,
                "Sgpt": 22, "Sgot": 24, "TP": 7.3, "ALB": 4.0, "A_G_Ratio": 1.2
            },
            "expected_risk": "Low Risk",
            "expected_positive": False
        },
        "High-Risk Sample": {
            "payload": {
                "Age": 58, "Gender": "Male", "TB": 6.8, "DB": 3.4, "Alkphos": 490,
                "Sgpt": 145, "Sgot": 160, "TP": 5.6, "ALB": 2.4, "A_G_Ratio": 0.7
            },
            "expected_risk": "High Risk",
            "expected_positive": True
        }
    },
    "lung": {
        "Low-Risk Sample": {
            "payload": {
                "GENDER": "Female", "AGE": 32, "SMOKING": "No", "YELLOW_FINGERS": "No",
                "ANXIETY": "No", "PEER_PRESSURE": "No", "CHRONIC_DISEASE": "No",
                "FATIGUE": "No", "ALLERGY": "No", "WHEEZING": "No", "ALCOHOL_CONSUMING": "No",
                "COUGHING": "No", "SHORTNESS_OF_BREATH": "No", "SWALLOWING_DIFFICULTY": "No",
                "CHEST_PAIN": "No"
            },
            "expected_risk": "Low Risk",
            "expected_positive": False
        },
        "High-Risk Sample": {
            "payload": {
                "GENDER": "Male", "AGE": 68, "SMOKING": "Yes", "YELLOW_FINGERS": "Yes",
                "ANXIETY": "Yes", "PEER_PRESSURE": "Yes", "CHRONIC_DISEASE": "Yes",
                "FATIGUE": "Yes", "ALLERGY": "No", "WHEEZING": "Yes", "ALCOHOL_CONSUMING": "Yes",
                "COUGHING": "Yes", "SHORTNESS_OF_BREATH": "Yes", "SWALLOWING_DIFFICULTY": "Yes",
                "CHEST_PAIN": "Yes"
            },
            "expected_risk": "High Risk",
            "expected_positive": True
        }
    },
    "breast_cancer": {
        "Low-Risk Sample": {
            "payload": {
                "mean_radius": 11.8, "mean_texture": 16.2, "mean_perimeter": 75.8, "mean_area": 427.0,
                "mean_smoothness": 0.086, "mean_compactness": 0.058, "mean_concavity": 0.024,
                "mean_concave_points": 0.018, "mean_symmetry": 0.165, "mean_fractal_dimension": 0.059
            },
            "expected_risk": "Low Risk",
            "expected_positive": False
        },
        "High-Risk Sample": {
            "payload": {
                "mean_radius": 20.6, "mean_texture": 25.5, "mean_perimeter": 138.0, "mean_area": 1320.0,
                "mean_smoothness": 0.118, "mean_compactness": 0.235, "mean_concavity": 0.280,
                "mean_concave_points": 0.145, "mean_symmetry": 0.240, "mean_fractal_dimension": 0.078
            },
            "expected_risk": "High Risk",
            "expected_positive": True
        }
    }
}

def test_all_modules():
    print("=" * 75)
    print(" MULTI-DISEASE PREDICTION SYSTEM — PREDICTION ENGINE TEST SUITE ")
    print("=" * 75)

    passed_count = 0
    total_count = 0

    for disease, scenarios in TEST_CASES.items():
        print(f"\n--- Testing Disease: {disease.upper()} ---")
        for sample_type, data in scenarios.items():
            total_count += 1
            res = predict_disease(disease, data["payload"])

            assert res["status"] == "success", f"Failed prediction for {disease} ({sample_type}): {res}"
            assert res["is_positive"] == data["expected_positive"], (
                f"Mismatch in {disease} ({sample_type}): expected {data['expected_positive']}, got {res['is_positive']}"
            )

            passed_count += 1
            print(f"  [PASS] {sample_type:18s} -> {res['result_label']:35s} | Conf: {res['confidence']:5.1f}% | Model: {res['model_name']}")

    print("\n" + "=" * 75)
    print(f" TEST SUITE SUMMARY: {passed_count}/{total_count} SCENARIOS PASSED (100% SUCCESS) ")
    print("=" * 75)

if __name__ == "__main__":
    test_all_modules()

