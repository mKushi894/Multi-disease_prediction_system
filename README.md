# 🩺 Multi-Disease Prediction System

**Major Project — Department of Computer Science and Engineering**  
**Institution:** R R Institute of Technology (AICTE Approved, VTU Affiliated, NAAC A+, NBA Accredited)  
**Project Guide:** Dr. Manjunath R, Professor & HOD, Dept. of CSE, RRIT  
**Team (Group 17):**
* M Kushala (1RI23CS078)
* Prajwal Aravind D M (1RI23CS108)
* Sameeksha M G (1RI23CS128)
* Shiva Prakash T R (1RI23CS134)

---

## 📖 Executive Summary

The **Multi-Disease Prediction System** is a unified, intelligent healthcare web application that performs preliminary risk screening across five major chronic diseases using Classical Machine Learning pipelines:

1. ❤️ **Heart Disease** (Cardiovascular risk assessment from resting vitals, ECG, and stress test diagnostics)
2. 🫘 **Chronic Kidney Disease (CKD)** (Renal filtration status from comprehensive urinalysis, blood chemistry, and comorbidities)
3. 🫀 **Liver Disease** (Hepatic impairment and biomarker profile from liver enzymes, bilirubin, and serum protein ratios)
4. 🫁 **Lung Disease** (Respiratory and cancer risk classification from lifestyle exposure and chronic symptomatic patterns)
5. 🎗️ **Breast Cancer** (Diagnostic malignancy classification from digitized Fine Needle Aspirate nuclear morphology)

Built using **Python 3.11**, **Scikit-Learn**, and **Streamlit**, the application delivers instant risk stratification, model prediction confidence percentages, clinical guidance notes, and dynamic access to underlying model evaluation metrics.

---

## 🏛️ System Architecture

```text
multi-disease-prediction-system/
├── app.py                          # Main Streamlit Dashboard & Navigation Hub
│
├── pages/                          # Multi-Page Interface
│   ├── 1_Heart_Disease.py          # Cardiovascular Risk Module
│   ├── 2_Kidney_Disease.py         # Chronic Kidney Disease Module
│   ├── 3_Liver_Disease.py          # Hepatic Impairment Module
│   ├── 4_Lung_Disease.py           # Respiratory & Lung Disease Module
│   └── 5_Breast_Cancer.py          # Breast Cancer Diagnostic Module
│
├── src/
│   ├── preprocessing/              # Feature Transformation & Cleaning
│   │   ├── heart_preprocessing.py
│   │   ├── kidney_preprocessing.py
│   │   ├── liver_preprocessing.py
│   │   ├── lung_preprocessing.py
│   │   └── breast_cancer_preprocessing.py
│   │
│   ├── training/                   # Offline Model Training & Comparison Scripts
│   │   ├── train_heart.py
│   │   ├── train_kidney.py
│   │   ├── train_liver.py
│   │   ├── train_lung.py
│   │   └── train_breast_cancer.py
│   │
│   ├── prediction/                 # Unified Inference Engine
│   │   └── predict.py
│   │
│   └── utils/                      # Validation, UI Components & Constants
│       ├── constants.py
│       ├── validation.py
│       ├── ui_components.py
│       ├── download_datasets.py
│       └── test_engine.py
│
├── models/                         # Serialized Model Pipelines & Live Metrics
│   ├── heart/                      # model.pkl, metadata.json
│   ├── kidney/                     # model.pkl, metadata.json
│   ├── liver/                      # model.pkl, metadata.json
│   ├── lung/                       # model.pkl, metadata.json
│   └── breast_cancer/              # model.pkl, metadata.json
│
├── datasets/
│   ├── raw/                        # 5x Original Public Benchmark CSVs
│   ├── processed/                  # 5x Cleaned Datasets
│   └── README.md                   # Dataset Provenance & Preprocessing Specs
│
├── requirements.txt                # Dependency Manifest
├── PRD.md                          # Master Product Requirements Document
└── README.md                       # Project Documentation
```

---

## 📊 Machine Learning Models & Measured Benchmark Performance

All models were evaluated using an 80/20 stratified train-test split against 6 candidate algorithms (*Logistic Regression, Decision Tree, Random Forest, Support Vector Machine, K-Nearest Neighbors, Gradient Boosting*). Preprocessing (scaling and imputation) is strictly encapsulated inside scikit-learn `Pipeline` objects to ensure zero data leakage.

| Disease Module | Selected Algorithm | Test Accuracy | Precision | Recall | F1-Score | ROC-AUC | Test Sample Size |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| ❤️ **Heart Disease** | Logistic Regression | **85.25%** | 85.19% | 82.14% | **83.64%** | **0.9242** | 61 records |
| 🫘 **Kidney Disease (CKD)** | Random Forest Classifier | **100.00%** | 100.00% | 100.00% | **100.00%** | **1.0000** | 80 records |
| 🫀 **Liver Disease (ILPD)** | Logistic Regression | **73.50%** | 74.07% | 96.39% | **83.77%** | **0.8306** | 117 records |
| 🫁 **Lung Disease** | K-Nearest Neighbors | **89.29%** | 90.38% | 97.92% | **94.00%** | **0.9375** | 56 records |
| 🎗️ **Breast Cancer (WDBC)** | Support Vector Machine | **95.61%** | 97.44% | 90.48% | **93.83%** | **0.9828** | 114 records |

*Note on CKD:* Chronic Kidney Disease markers (e.g. serum creatinine, hemoglobin, albumin) provide strong separation in the UCI dataset, verified by 99.25% (±0.6%) 5-fold cross-validation.  
*Note on Lung Disease:* Evaluated on the deduplicated dataset of 276 unique patient responses to eliminate duplicate train-test contamination.

---

## 🚀 Quickstart & Setup Instructions

### 1. Prerequisites
* Python 3.10 or 3.11 installed
* Windows PowerShell (or Linux/macOS terminal)

### 2. Environment Setup
```powershell
# Create Virtual Environment
python -m venv .venv

# Activate Virtual Environment (PowerShell)
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run Verification Test Suite
```powershell
python src\utils\test_engine.py
```

### 5. Launch the Streamlit Web Application
```powershell
streamlit run app.py
```

The application will launch automatically in your web browser at `http://localhost:8501`.

---

## 🎓 Viva & Project Demonstration Guide

Follow this 5-minute flow during your project presentation:

```text
1. Open Dashboard (http://localhost:8501)
   └── Showcase system overview, 5 disease cards, and live system metrics
2. Select a Disease Module (e.g., Heart Disease or Kidney Disease)
   └── Explain clinical input parameters and units
3. Click "🟢 Load Low-Risk Sample" -> Click "Run Prediction"
   └── Show "Low Risk" result badge, probability gauge, and lifestyle advice
4. Click "🔴 Load High-Risk Sample" -> Click "Run Prediction"
   └── Show "High Risk" alert, probability percentage, and clinical referral advice
5. Open "📊 Model Information & Performance Metrics" Expander
   └── Present the confusion matrix, algorithm comparison table, and evaluation metrics
```

---

## 🧪 Automated Testing

To run the complete automated test suite verifying all 10 presets across all 5 disease modules:
```powershell
python src\utils\test_engine.py
```

---

## ☁️ Streamlit Community Cloud Deployment Guide

This repository is optimized for one-click deployment on **Streamlit Community Cloud**:

1. Log in to [share.streamlit.io](https://share.streamlit.io/) with your GitHub account.
2. Click **"New app"** or **"Create app"**.
3. Select your repository: `<your-github-user>/Multi-Disease-Prediction-System`.
4. Configure the deployment settings:
   * **Branch:** `main`
   * **Main file path:** `app.py`
   * **App URL (optional):** `multi-disease-prediction-system` (or custom subdomain)
5. Click **"Deploy!"**.

Streamlit Cloud will automatically detect `requirements.txt`, install all required dependencies, load the serialized model pipelines, and launch the live web application on a public URL.

---

## 🔐 Authentication, History & AI Assistant (Optional)

The app supports optional user login (Supabase) and a Gemini-powered AI assistant.  
When Supabase is not configured, the app runs anonymously with ML predictions still working.

1. Create a Supabase project and run `supabase/schema.sql` in the SQL Editor. It creates `profiles`, `diagnosis_runs`, `chat_messages`, and `feedback` with RLS policies.
2. Create a Gemini API key in Google AI Studio.
3. Add secrets (locally: `.streamlit/secrets.toml`; on Streamlit Cloud: App → Settings → Secrets):

```toml
SUPABASE_URL = "https://YOUR-PROJECT.supabase.co"
SUPABASE_ANON_KEY = "YOUR-ANON-KEY"
GEMINI_API_KEY = "YOUR-GEMINI-API-KEY"
```

A template is provided at `.streamlit/secrets.toml.example`.

## ⚠️ Important Medical Disclaimer

> **Medical Disclaimer:** This Multi-Disease Prediction System is an academic machine-learning prototype developed for educational and demonstration purposes. It is **NOT** a certified medical device, and its predictions are **NOT** a substitute for professional clinical diagnosis, clinical judgment, advice, or treatment. Predictions are statistical estimates generated from trained algorithms on research datasets. Always consult a qualified healthcare professional for any medical concerns or diagnostic evaluations.
