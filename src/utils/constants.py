"""
Constants, schema definitions, and medical disclaimers for Multi-Disease Prediction System.
"""

MEDICAL_DISCLAIMER = (
    "Medical Disclaimer: This Multi-Disease Prediction System is an academic machine-learning prototype "
    "developed for educational and demonstration purposes. It is NOT a certified medical device, and its "
    "predictions are NOT a substitute for professional medical diagnosis, clinical judgment, advice, or treatment. "
    "Predictions are statistical estimates generated from trained algorithms on research datasets. Always consult a qualified "
    "healthcare professional for any medical concerns or diagnostic evaluations."
)

APP_TITLE = "Multi-Disease Prediction System"
APP_SUBTITLE = "AI-Assisted Multi-Organ Health Risk Screening Dashboard"

DISEASE_METADATA = {
    "heart": {
        "id": "heart",
        "name": "Heart Disease",
        "icon": "❤️",
        "short_desc": "Evaluates cardiovascular risk based on patient vitals, ECG findings, and stress test metrics.",
        "page_file": "pages/1_Heart_Disease.py",
        "positive_label": "High Risk of Heart Disease",
        "negative_label": "Low Risk of Heart Disease",
        "positive_desc": "The model indicates statistical indicators associated with cardiovascular abnormalities. Prompt consultation with a cardiologist is advised.",
        "negative_desc": "Parameters fall within typical baseline cardiovascular ranges. Maintain heart-healthy lifestyle habits."
    },
    "kidney": {
        "id": "kidney",
        "name": "Chronic Kidney Disease",
        "icon": "🫘",
        "short_desc": "Screens for Chronic Kidney Disease (CKD) using comprehensive blood, urine, and metabolic biomarkers.",
        "page_file": "pages/2_Kidney_Disease.py",
        "positive_label": "Chronic Kidney Disease (CKD) Likely",
        "negative_label": "Chronic Kidney Disease (CKD) Unlikely",
        "positive_desc": "Biomarkers indicate potential renal filtration compromise. Renal function tests (eGFR, ultrasound) are recommended.",
        "negative_desc": "Kidney filtration markers and urinalysis metrics align with typical healthy baseline values."
    },
    "liver": {
        "id": "liver",
        "name": "Liver Disease",
        "icon": "🫀",
        "short_desc": "Assesses hepatic impairment and liver disease risk from liver enzymes, bilirubin, and protein ratios.",
        "page_file": "pages/3_Liver_Disease.py",
        "positive_label": "Liver Disease Risk Detected",
        "negative_label": "Normal Liver Biomarker Profile",
        "positive_desc": "Enzyme or bilirubin profiles show elevation consistent with hepatic strain. Further hepatology evaluation is suggested.",
        "negative_desc": "Hepatic enzyme levels and protein fractions are within normal clinical thresholds."
    },
    "lung": {
        "id": "lung",
        "name": "Lung Disease",
        "icon": "🫁",
        "short_desc": "Analyzes respiratory risk based on lifestyle exposure, chronic symptoms, and clinical indicators.",
        "page_file": "pages/4_Lung_Disease.py",
        "positive_label": "High Risk of Lung Disease",
        "negative_label": "Low Risk of Lung Disease",
        "positive_desc": "Symptom and lifestyle profile indicates elevated respiratory risk. Pulmonary function testing or specialist review is advised.",
        "negative_desc": "Reported symptoms and environmental exposures indicate a low preliminary risk profile."
    },
    "breast_cancer": {
        "id": "breast_cancer",
        "name": "Breast Cancer",
        "icon": "🎗️",
        "short_desc": "Classifies cell nucleus characteristics from fine needle aspirate (FNA) diagnostic measurements.",
        "page_file": "pages/5_Breast_Cancer.py",
        "positive_label": "Malignant Characteristics Detected",
        "negative_label": "Benign / Non-Malignant Profile",
        "positive_desc": "Cell morphological measurements indicate characteristics consistent with malignancy. Immediate histopathological correlation is required.",
        "negative_desc": "Cell nuclei morphometry aligns with benign tissue samples. Routine regular screening remains recommended."
    }
}

# Heart Disease UI Field Definitions
HEART_FIELDS = {
    "age": {"label": "Age", "type": "number", "min": 18, "max": 100, "default": 54, "unit": "years", "help": "Patient age in years"},
    "sex": {"label": "Sex", "type": "select", "options": ["Male", "Female"], "default": "Male", "help": "Biological sex of patient"},
    "cp": {"label": "Chest Pain Type", "type": "select", "options": ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"], "default": "Typical Angina", "help": "Nature of chest discomfort"},
    "trestbps": {"label": "Resting Blood Pressure", "type": "number", "min": 80, "max": 200, "default": 130, "unit": "mm Hg", "help": "Resting BP on admission"},
    "chol": {"label": "Serum Cholesterol", "type": "number", "min": 100, "max": 600, "default": 240, "unit": "mg/dl", "help": "Total cholesterol in serum"},
    "fbs": {"label": "Fasting Blood Sugar > 120 mg/dl", "type": "select", "options": ["No", "Yes"], "default": "No", "help": "Elevated fasting blood sugar indicator"},
    "restecg": {"label": "Resting ECG Results", "type": "select", "options": ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"], "default": "Normal", "help": "Electrocardiographic findings"},
    "thalach": {"label": "Max Heart Rate Achieved", "type": "number", "min": 60, "max": 220, "default": 150, "unit": "bpm", "help": "Maximum heart rate under stress test"},
    "exang": {"label": "Exercise-Induced Angina", "type": "select", "options": ["No", "Yes"], "default": "No", "help": "Angina triggered by exercise"},
    "oldpeak": {"label": "ST Depression (Oldpeak)", "type": "float", "min": 0.0, "max": 6.5, "default": 1.0, "step": 0.1, "unit": "mm", "help": "ST depression induced by exercise relative to rest"},
    "slope": {"label": "Slope of Peak Exercise ST", "type": "select", "options": ["Upsloping", "Flat", "Downsloping"], "default": "Flat", "help": "Slope profile of peak ST segment"},
    "ca": {"label": "Number of Major Vessels (0-4)", "type": "number", "min": 0, "max": 4, "default": 0, "unit": "vessels", "help": "Vessels colored by fluoroscopy"},
    "thal": {"label": "Thalassemia Status", "type": "select", "options": ["Normal", "Fixed Defect", "Reversible Defect"], "default": "Normal", "help": "Thalassemia blood disorder diagnostic classification"}
}

# Liver Disease UI Field Definitions
LIVER_FIELDS = {
    "Age": {"label": "Age", "type": "number", "min": 4, "max": 95, "default": 45, "unit": "years", "help": "Age of the patient"},
    "Gender": {"label": "Gender", "type": "select", "options": ["Male", "Female"], "default": "Male", "help": "Patient gender"},
    "TB": {"label": "Total Bilirubin (TB)", "type": "float", "min": 0.4, "max": 75.0, "default": 1.2, "step": 0.1, "unit": "mg/dl", "help": "Normal range: 0.2 - 1.2 mg/dl"},
    "DB": {"label": "Direct Bilirubin (DB)", "type": "float", "min": 0.1, "max": 20.0, "default": 0.4, "step": 0.1, "unit": "mg/dl", "help": "Conjugated bilirubin level"},
    "Alkphos": {"label": "Alkaline Phosphatase (ALP)", "type": "number", "min": 60, "max": 2200, "default": 200, "unit": "IU/L", "help": "Liver enzyme biomarker"},
    "Sgpt": {"label": "Alamine Aminotransferase (ALT / SGPT)", "type": "number", "min": 10, "max": 2000, "default": 35, "unit": "IU/L", "help": "Serum glutamic pyruvic transaminase"},
    "Sgot": {"label": "Aspartate Aminotransferase (AST / SGOT)", "type": "number", "min": 10, "max": 5000, "default": 40, "unit": "IU/L", "help": "Serum glutamic oxaloacetic transaminase"},
    "TP": {"label": "Total Proteins (TP)", "type": "float", "min": 2.5, "max": 10.0, "default": 6.8, "step": 0.1, "unit": "g/dl", "help": "Total protein content in blood"},
    "ALB": {"label": "Albumin (ALB)", "type": "float", "min": 0.8, "max": 6.0, "default": 3.4, "step": 0.1, "unit": "g/dl", "help": "Albumin concentration in serum"},
    "A_G_Ratio": {"label": "Albumin/Globulin Ratio (A/G)", "type": "float", "min": 0.3, "max": 3.0, "default": 1.0, "step": 0.05, "unit": "ratio", "help": "Ratio of albumin to globulins"}
}

# Kidney Disease UI Field Definitions
KIDNEY_FIELDS = {
    "age": {"label": "Age", "type": "number", "min": 1, "max": 100, "default": 50, "unit": "years"},
    "bp": {"label": "Blood Pressure", "type": "number", "min": 50, "max": 180, "default": 80, "unit": "mm Hg"},
    "sg": {"label": "Specific Gravity", "type": "select", "options": ["1.005", "1.010", "1.015", "1.020", "1.025"], "default": "1.020"},
    "al": {"label": "Albumin", "type": "select", "options": ["0", "1", "2", "3", "4", "5"], "default": "0"},
    "su": {"label": "Sugar", "type": "select", "options": ["0", "1", "2", "3", "4", "5"], "default": "0"},
    "rbc": {"label": "Red Blood Cells in Urine", "type": "select", "options": ["Normal", "Abnormal"], "default": "Normal"},
    "pc": {"label": "Pus Cell in Urine", "type": "select", "options": ["Normal", "Abnormal"], "default": "Normal"},
    "pcc": {"label": "Pus Cell Clumps", "type": "select", "options": ["Not Present", "Present"], "default": "Not Present"},
    "ba": {"label": "Bacteria in Urine", "type": "select", "options": ["Not Present", "Present"], "default": "Not Present"},
    "bgr": {"label": "Blood Glucose Random", "type": "number", "min": 20, "max": 500, "default": 120, "unit": "mg/dl"},
    "bu": {"label": "Blood Urea", "type": "float", "min": 1.5, "max": 400.0, "default": 40.0, "step": 1.0, "unit": "mg/dl"},
    "sc": {"label": "Serum Creatinine", "type": "float", "min": 0.4, "max": 80.0, "default": 1.1, "step": 0.1, "unit": "mg/dl"},
    "sod": {"label": "Sodium", "type": "float", "min": 4.5, "max": 165.0, "default": 138.0, "step": 0.5, "unit": "mEq/L"},
    "pot": {"label": "Potassium", "type": "float", "min": 2.5, "max": 50.0, "default": 4.2, "step": 0.1, "unit": "mEq/L"},
    "hemo": {"label": "Hemoglobin", "type": "float", "min": 3.0, "max": 18.0, "default": 14.5, "step": 0.1, "unit": "g/dl"},
    "pcv": {"label": "Packed Cell Volume", "type": "number", "min": 9, "max": 55, "default": 42, "unit": "%"},
    "wbcc": {"label": "White Blood Cell Count", "type": "number", "min": 2000, "max": 27000, "default": 8000, "unit": "cells/cumm"},
    "rbcc": {"label": "Red Blood Cell Count", "type": "float", "min": 2.0, "max": 8.0, "default": 5.0, "step": 0.1, "unit": "m/cumm"},
    "htn": {"label": "Hypertension History", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "dm": {"label": "Diabetes Mellitus", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "cad": {"label": "Coronary Artery Disease", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "appet": {"label": "Appetite", "type": "select", "options": ["Good", "Poor"], "default": "Good"},
    "pe": {"label": "Pedal Edema (Swelling)", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "ane": {"label": "Anemia Diagnosed", "type": "select", "options": ["No", "Yes"], "default": "No"}
}

# Lung Disease UI Field Definitions
LUNG_FIELDS = {
    "GENDER": {"label": "Gender", "type": "select", "options": ["Male", "Female"], "default": "Male"},
    "AGE": {"label": "Age", "type": "number", "min": 18, "max": 100, "default": 60, "unit": "years"},
    "SMOKING": {"label": "Smoking Habit", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "YELLOW_FINGERS": {"label": "Yellow Fingers", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "ANXIETY": {"label": "Anxiety Symptoms", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "PEER_PRESSURE": {"label": "Peer Pressure Exposure", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "CHRONIC_DISEASE": {"label": "Chronic Respiratory / Other Disease", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "FATIGUE": {"label": "Persistent Fatigue", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "ALLERGY": {"label": "Known Allergies", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "WHEEZING": {"label": "Wheezing / Stridor", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "ALCOHOL_CONSUMING": {"label": "Regular Alcohol Consumption", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "COUGHING": {"label": "Chronic Coughing", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "SHORTNESS_OF_BREATH": {"label": "Shortness of Breath (Dyspnea)", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "SWALLOWING_DIFFICULTY": {"label": "Swallowing Difficulty (Dysphagia)", "type": "select", "options": ["No", "Yes"], "default": "No"},
    "CHEST_PAIN": {"label": "Chest Pain / Discomfort", "type": "select", "options": ["No", "Yes"], "default": "No"}
}

# Breast Cancer UI Field Definitions (Core 10 Diagnostic Mean Features)
BREAST_CANCER_FIELDS = {
    "mean_radius": {"label": "Mean Radius", "type": "float", "min": 6.0, "max": 30.0, "default": 14.1, "step": 0.1, "unit": "mm", "help": "Mean of distances from center to contour points"},
    "mean_texture": {"label": "Mean Texture", "type": "float", "min": 9.0, "max": 40.0, "default": 19.3, "step": 0.1, "unit": "gray-scale", "help": "Standard deviation of gray-scale values"},
    "mean_perimeter": {"label": "Mean Perimeter", "type": "float", "min": 40.0, "max": 190.0, "default": 92.0, "step": 0.5, "unit": "mm", "help": "Mean perimeter of cell nucleus"},
    "mean_area": {"label": "Mean Area", "type": "float", "min": 140.0, "max": 2500.0, "default": 654.0, "step": 1.0, "unit": "mm²", "help": "Mean area of cell nucleus"},
    "mean_smoothness": {"label": "Mean Smoothness", "type": "float", "min": 0.05, "max": 0.16, "default": 0.096, "step": 0.001, "unit": "score", "help": "Local variation in radius lengths"},
    "mean_compactness": {"label": "Mean Compactness", "type": "float", "min": 0.02, "max": 0.35, "default": 0.104, "step": 0.001, "unit": "score", "help": "Perimeter^2 / area - 1.0"},
    "mean_concavity": {"label": "Mean Concavity", "type": "float", "min": 0.0, "max": 0.45, "default": 0.088, "step": 0.001, "unit": "score", "help": "Severity of concave portions of contour"},
    "mean_concave_points": {"label": "Mean Concave Points", "type": "float", "min": 0.0, "max": 0.20, "default": 0.048, "step": 0.001, "unit": "score", "help": "Number of concave portions of contour"},
    "mean_symmetry": {"label": "Mean Symmetry", "type": "float", "min": 0.10, "max": 0.30, "default": 0.181, "step": 0.001, "unit": "score", "help": "Symmetry measurement of nucleus"},
    "mean_fractal_dimension": {"label": "Mean Fractal Dimension", "type": "float", "min": 0.05, "max": 0.10, "default": 0.062, "step": 0.001, "unit": "score", "help": "Coastline approximation - 1"}
}
