# Multi-Disease Prediction System

**Project:** Major Project — Department of Computer Science and Engineering
**Institution:** R R Institute of Technology (AICTE approved, VTU affiliated, NAAC A+, NBA accredited)
**Guide:** Dr. Manjunath R, Professor & HOD, Dept. of CSE, RRIT
**Team (Group 17):** M Kushala (1RI23CS078) · Prajwal Aravind D M (1RI23CS108) · Sameeksha M G (1RI23CS128) · Shiva Prakash T R (1RI23CS134)

**Document type:** Product Requirements Document (PRD) — Master Blueprint for Autonomous AI Coding Agent
**Version:** 1.0
**Status:** Approved for implementation

---

## 1. Executive Summary

The Multi-Disease Prediction System is a unified, web-based machine learning application that predicts the likelihood of five diseases — **Heart Disease, Kidney Disease, Liver Disease, Lung Disease, and Breast Cancer** — from patient-entered clinical parameters. Instead of five disconnected tools, the system offers one dashboard where a user selects a disease, fills in a short clinical form, and receives an instant ML-based risk prediction with a confidence score, all through a single Streamlit web application.

This PRD translates the source PowerPoint (project synopsis: "Multi Disease Prediction System for Liver, Heart, Kidney, Lungs and Breast Cancer," Group 17, RRIT) into a buildable engineering specification. The PPT's academic framing — including references to genetic datasets, CT-scan imaging, IoT integration, and cloud storage — is preserved as *motivating context and future scope*, but the **MVP that must actually be built** uses five structured/tabular datasets and classical ML models (Logistic Regression, Random Forest, Decision Tree, SVM, KNN, Gradient Boosting), trained offline and served through a Streamlit interface. This is the same architecture the PPT's own literature survey shows working successfully in comparable published systems (e.g., reference [1] in the literature survey achieves 95–99% accuracy on Kidney/Breast Cancer/Heart Disease using exactly this tabular + classical-ML + Streamlit approach).

The result is a fully working, visually polished, demoable prototype that an AI coding agent can build end-to-end from this document without needing further clarification.

---

## 2. Problem Statement

Early detection of chronic and life-threatening diseases — lung disease, heart disease, kidney disease, liver disease, and breast cancer — significantly improves patient outcomes, but existing detection pathways are fragmented and often too slow:

- **Heart Disease:** Diagnosis frequently happens late, and reliably depends on hospital-based testing infrastructure that isn't always accessible.
- **Kidney Disease:** Low public awareness means Chronic Kidney Disease (CKD) is often diagnosed only at a late, harder-to-treat stage.
- **Liver Disease:** Symptoms are non-specific and biomarker data is inconsistent, making early risk identification difficult.
- **Lung Disease:** Genetic and environmental risk patterns are complex, and high-quality, accessible datasets are limited.
- **Breast Cancer:** Manual screening and interpretation are error-prone and can delay tumor detection.

Existing ML-based tools (surveyed in Chapter 3 of the source PPT) mostly predict **one disease at a time**, run on different platforms, and are trained on small, localized datasets (e.g., 416 patients for liver disease, 606 for heart disease). This fragmentation increases the effort and infrastructure needed to get a holistic risk picture and limits reach, especially in resource-limited settings.

**The core problem this project solves:** there is no single, easy-to-use platform where a patient or clinician can check risk across all five of these high-impact diseases using structured clinical data they already have (lab values, vitals, diagnostic measurements).

---

## 3. Project Objectives

Carried forward directly from the PPT's Chapter 1.2, translated into engineering objectives:

1. **Data Objective:** Acquire and prepare clean, well-documented, structured clinical datasets with relevant parameters for all five diseases, sufficient to train reliable classical ML models.
2. **Design Objective:** Build one unified system architecture — shared preprocessing pipeline pattern, shared UI shell, disease-specific model modules — so all five diseases are served through a single consistent application rather than five separate tools.
3. **Implementation Objective:** Train, evaluate, select, and serialize the best-performing model per disease using Python's standard ML stack, and integrate all five into one Streamlit frontend.
4. **Testing Objective:** Validate every model using accuracy, precision, recall, F1-score (and ROC-AUC where applicable), and validate the application itself through functional testing (forms, navigation, predictions, error handling) and basic user acceptance testing (can a non-technical evaluator use it unaided during a demo?).
5. **Demonstration Objective:** Produce a system that can be confidently demonstrated end-to-end in a college evaluation setting within a few minutes, covering all five diseases.

---

## 4. Scope

### 4.1 In Scope (MVP)
- Five independent disease-prediction modules (Heart, Kidney, Liver, Lung, Breast Cancer), each backed by a trained classical ML model on structured/tabular data.
- A single-page-application-style Streamlit dashboard with navigation between a home page and the five prediction pages.
- Full ML pipeline: data acquisition → cleaning → preprocessing → training → evaluation → model comparison → serialization.
- Input validation, medical disclaimers, result visualization (label + probability/confidence), and basic model-info display per disease.
- Local execution (`streamlit run app.py`) — no deployment infrastructure required for the demo, though the app is deployment-ready.

### 4.2 Out of Scope (MVP) — Explicitly Deferred to Future Scope
- Medical image analysis (CT scans, X-rays, mammograms) via CNN.
- Genetic-data-based prediction.
- IoT / wearable device integration.
- Cloud storage, hospital-system integration, or telemedicine platform integration.
- User authentication, patient accounts, or prediction history/database persistence.
- Multi-language support, doctor dashboards, explainable-AI visualizations (SHAP/LIME).

### 4.3 Scope Statement (as inherited from PPT, Section 1.3)
- **Medical scope:** Covers five diseases with high global health impact.
- **Operational scope:** Web-accessible, reducing dependency on in-person hospital visits for an initial risk check.
- **Research scope:** Demonstrates that combining structured data with well-chosen classical ML algorithms can produce strong, explainable predictive accuracy (consistent with the literature survey's findings, where classical models like Random Forest and Gradient Boosting reach 90–99% accuracy on comparable tabular datasets).
- **Societal scope:** Improves access to a first-pass health risk indicator, particularly useful where specialist access is limited.

---

## 5. Target Users

| User type | Use case |
|---|---|
| **College evaluators / examiners** | Primary audience for the demo; need a working, understandable, visually convincing system. |
| **Students (project team)** | Build, train, and present the system; need clear module boundaries to divide work. |
| **Illustrative end users (in the demo narrative)** | Patients checking preliminary risk, and clinicians using it as a fast decision-support aid — but the actual deployed audience for a college project is the evaluation panel, not real patients. |

---

## 6. Proposed Solution

A single Streamlit multi-page web application, **Multi-Disease Prediction System**, structured as:

1. **Home/Dashboard page** — introduces the project, lists the five diseases as clickable cards, states the tech stack, and shows the medical disclaimer.
2. **Five prediction pages** — one per disease, each with a form matching that disease's clinical parameters, a "Predict" action, and a result panel showing the prediction, a risk label (e.g., Low Risk / High Risk), and a confidence percentage where the underlying model supports `predict_proba`.
3. **Shared ML backend** — each disease has its own dataset, its own preprocessing pipeline (fit once, saved as a scaler/encoder object), its own trained model (chosen by comparing several candidate algorithms on validation performance), and its own serialized artifacts (`.pkl` files) loaded at runtime by the Streamlit app.
4. **Offline training pipeline** — a set of Python training scripts (run once, ahead of the demo) that produce the serialized models and preprocessing objects consumed by the live app. The live Streamlit app performs **no training at request time** — only inference — which keeps the UI fast and reliable during a demo.

This directly implements the four-layer architecture described in the PPT (Section 5.2 System Architecture): UI Layer → Data Processing Layer → Machine Learning Layer → Storage/Model Layer.

---

## 7. MVP Definition

### 7.1 What "done" means for the MVP
A user can open the app locally, land on the dashboard, click into any of the five disease modules, fill in that disease's form with plausible values, click Predict, and see a clear result (label + confidence) within roughly one second, with no crashes, for all five diseases, using models trained on real public datasets and evaluated with standard metrics.

### 7.2 MVP Disease-by-Dataset Mapping (Key Implementation Decision)

The PPT mentions genetic data, medical images, CT scans, and CNNs as techniques literature-survey papers used. Building and reliably training an image-based CNN (e.g., for CT-scan lung cancer detection) within a college-project timeframe is high-risk: it requires large labeled image datasets, GPU training time, and careful validation to avoid misleading accuracy claims. This PRD makes the explicit engineering decision to build **all five modules on structured/tabular data** for the MVP:

| Disease | MVP data type | Rationale |
|---|---|---|
| Heart Disease | Tabular clinical data | Directly matches PPT Implementation section (Slide 28) and literature survey (13-attribute datasets, ~80–95% accuracy achieved with classical ML). |
| Kidney Disease | Tabular clinical data | PPT literature survey explicitly cites a 25-attribute Kaggle CKD dataset achieving 98% accuracy with Decision Tree/Random Forest/Gradient Boosting — directly reusable approach. |
| Liver Disease | Tabular clinical data | PPT literature survey and Slide 28 both reference the Indian Liver Patient Dataset (583 records) achieving ~90% accuracy with classical ML. |
| Breast Cancer | Tabular diagnostic data | PPT Implementation section (Slide 28) explicitly lists Breast Cancer as a tabular target; Wisconsin Diagnostic Breast Cancer dataset is the standard, well-known choice. |
| Lung Disease | Tabular clinical/survey data (**not CT-scan imaging**) | The PPT's own Slide 28 Implementation list only commits to Heart, Liver, and Breast Cancer with certainty and treats Lung/Kidney as extensions elsewhere in the deck — this is the inconsistency the PRD must resolve. Rather than attempting a CNN on CT-scan data (high risk, needs an imaging dataset and GPU training time not guaranteed to be available), the MVP uses a **tabular lung cancer risk-survey dataset** (symptom/lifestyle-based, e.g., smoking status, age, chronic disease, fatigue, coughing, shortness of breath, chest pain — the well-known "Lung Cancer Survey" style dataset). This keeps Lung Disease consistent with the rest of the system's architecture and realistically buildable. |

**Resolved inconsistency:** The PPT's Slide 28 ("Implementation") only explicitly names Heart, Liver, and Breast Cancer, while the rest of the document (title, objectives, scope, architecture, Slide 24 System Overview) consistently commits to all five diseases. This PRD resolves that gap in favor of the document-wide five-disease commitment (matching the explicit instruction in the project brief), and defines Kidney and Lung as full tabular modules built with the same pipeline pattern as Heart/Liver/Breast Cancer.

**No CNNs, no CT-scan image classification, no genetic-marker datasets, and no IoT integration are part of the MVP.** These remain valid, clearly labeled Future Enhancements (Section 22).

### 7.3 Accuracy Claims Policy
No fixed accuracy number is promised in advance. The literature survey shows comparable tabular models regularly reaching 85–99% accuracy, so that range is a reasonable **expectation**, not a guarantee. Actual accuracy must be measured after training on the real dataset for each disease and reported honestly in the model-info panel and final report — including if a given disease's dataset yields lower accuracy than others.

---

## 8. System Architecture

Four-layer architecture (matching and formalizing PPT Section 5.2):

```
┌─────────────────────────────────────────────────────────┐
│  1. USER INTERFACE LAYER  (Streamlit)                     │
│     - Home/Dashboard page                                 │
│     - 5x Disease prediction pages (forms + results)       │
│     - Input validation, disclaimers, result visualization │
└───────────────────────┬─────────────────────────────────┘
                         │  user input (dict of feature values)
┌───────────────────────▼─────────────────────────────────┐
│  2. DATA PROCESSING LAYER  (src/preprocessing)             │
│     - Load saved scaler/encoder per disease                │
│     - Clean, encode, scale the single input row             │
│     - Validate ranges before passing to model                │
└───────────────────────┬─────────────────────────────────┘
                         │  preprocessed feature vector
┌───────────────────────▼─────────────────────────────────┐
│  3. MACHINE LEARNING LAYER  (src/prediction)                │
│     - Load serialized best model per disease                │
│     - model.predict() + model.predict_proba()                │
│     - Return label + confidence                              │
└───────────────────────┬─────────────────────────────────┘
                         │  prediction + confidence
┌───────────────────────▼─────────────────────────────────┐
│  4. STORAGE / MODEL LAYER  (models/, datasets/)              │
│     - Raw + cleaned datasets (5x CSV)                        │
│     - Trained model artifacts (5x .pkl)                       │
│     - Preprocessing artifacts (scaler/encoder .pkl per disease)│
│     - Metrics/metadata (JSON) for model-info display           │
└─────────────────────────────────────────────────────────┘
```

**Note on the PPT's "Database Layer":** The PPT's Slide 25 calls Layer 4 a "Database Layer." For the MVP, this PRD implements it as a **filesystem-based model/artifact store** (CSV + pickle/joblib files), not a database server — appropriate for a local demoable prototype and consistent with the PPT's own software requirements (no database technology is listed in Slide 22). A relational database for prediction history is documented as a Future Enhancement (Section 22).

There is no live network training loop and no request-time retraining — training happens once, offline, before the demo, via standalone scripts under `src/training/`.

---

## 9. Technology Stack

Directly adopted from PPT Slide 22 (Software Requirements) and Slide 23 (Technologies Used), with the specific integration approach clarified:

| Layer | Technology | Notes |
|---|---|---|
| Programming language | Python 3.10+ | |
| Data handling | Pandas, NumPy | Cleaning, feature engineering |
| Classical ML | Scikit-learn | Logistic Regression, Random Forest, Decision Tree, SVM, KNN, Gradient Boosting |
| Deep learning libs | TensorFlow / Keras | Retained in `requirements.txt` per PPT software requirements, but **not required for the tabular MVP** — reserved for the CNN future-scope work. Do not block MVP delivery on installing/using these; they are optional for the demo build. |
| Model persistence | Joblib (preferred) / Pickle | One model file + one preprocessing artifact file per disease |
| Web framework / frontend | Streamlit (multi-page app) | Matches PPT Slide 22 exactly |
| IDE | VS Code | Development environment, no runtime impact |
| OS | Windows / Linux | Cross-platform; no OS-specific code |
| Version control | Git/GitHub | Recommended for team collaboration (not in PPT but standard practice) |

**Architecture decision:** Streamlit's native **multi-page app** feature (a `pages/` directory, each file becoming a sidebar-navigable page) is used instead of a custom router. This is simpler and faster to build than a Flask/Django + REST API split, matches the PPT's own recommended stack, and is easy to run locally for a demo — satisfying the "fast development, easy local execution, easy demonstration" priorities from the project brief.

---

## 10. Disease Modules

Each module below follows the same shape: input fields → validation rules → workflow → output format. All numeric ranges are realistic clinical ranges; the coding agent should use these as the basis for input widgets and validation, adjusting only if the finally-downloaded dataset's actual column ranges differ slightly (in which case, use the dataset's real min/max for range validation and note the change in `datasets/README.md`).

### 10.1 Heart Disease

**Reference dataset pattern:** UCI Heart Disease / Cleveland dataset style (13 attributes), matching PPT literature survey reference [17].

**Input fields:**

| Field | Type | Example range/values |
|---|---|---|
| age | integer | 18–100 |
| sex | categorical | Male / Female |
| chest pain type (cp) | categorical | Typical angina / Atypical angina / Non-anginal pain / Asymptomatic |
| resting blood pressure (trestbps) | integer (mm Hg) | 80–200 |
| serum cholesterol (chol) | integer (mg/dl) | 100–600 |
| fasting blood sugar > 120 mg/dl (fbs) | boolean | Yes/No |
| resting ECG results (restecg) | categorical | Normal / ST-T abnormality / LV hypertrophy |
| max heart rate achieved (thalach) | integer | 60–220 |
| exercise-induced angina (exang) | boolean | Yes/No |
| ST depression induced by exercise (oldpeak) | float | 0.0–6.5 |
| slope of peak exercise ST segment (slope) | categorical | Upsloping / Flat / Downsloping |
| number of major vessels colored by fluoroscopy (ca) | integer | 0–4 |
| thalassemia (thal) | categorical | Normal / Fixed defect / Reversible defect |

**Validation:** all numeric fields must be within the ranges above; categorical fields via dropdown/select (no free text, no invalid categories possible by construction); no field may be left blank — Predict button is disabled until the form is complete.

**Prediction workflow:** form → encode categoricals to the same scheme used at training time → scale numerics with the saved scaler → `model.predict()` / `model.predict_proba()` → map to "Low Risk of Heart Disease" / "High Risk of Heart Disease".

**Output format:** risk label, confidence %, short explanatory note ("This is a statistical estimate based on the parameters provided, not a clinical diagnosis"), disclaimer.

### 10.2 Kidney Disease

**Reference dataset pattern:** Kaggle Chronic Kidney Disease (CKD) dataset style (~25 attributes), matching PPT literature survey reference [7].

**Input fields (representative set — full 24–25 feature set to be used if the downloaded dataset provides it):**

| Field | Type | Example range/values |
|---|---|---|
| age | integer | 1–100 |
| blood pressure (bp) | integer (mm Hg) | 50–180 |
| specific gravity | float (categorical-like) | 1.005–1.025 |
| albumin | integer | 0–5 |
| sugar | integer | 0–5 |
| red blood cells | categorical | Normal / Abnormal |
| pus cell | categorical | Normal / Abnormal |
| pus cell clumps | categorical | Present / Not present |
| bacteria | categorical | Present / Not present |
| blood glucose random | integer (mg/dl) | 22–500 |
| blood urea | float (mg/dl) | 1.5–400 |
| serum creatinine | float (mg/dl) | 0.4–76 |
| sodium | float (mEq/L) | 4.5–163 |
| potassium | float (mEq/L) | 2.5–47 |
| hemoglobin | float (g/dl) | 3.1–17.8 |
| packed cell volume | integer | 9–54 |
| white blood cell count | integer | 2200–26400 |
| red blood cell count | float | 2.1–8.0 |
| hypertension | boolean | Yes/No |
| diabetes mellitus | boolean | Yes/No |
| coronary artery disease | boolean | Yes/No |
| appetite | categorical | Good / Poor |
| pedal edema | boolean | Yes/No |
| anemia | boolean | Yes/No |

**Validation:** numeric fields bounded to dataset-derived min/max; categoricals via dropdown; missing-value tolerant at training time (median/mode imputation) but the live form requires all fields filled for a clean single-row prediction.

**Prediction workflow:** same pattern as Heart Disease — encode, scale, predict, map to "CKD Likely" / "CKD Unlikely".

**Output format:** risk label, confidence %, disclaimer.

### 10.3 Liver Disease

**Reference dataset pattern:** Indian Liver Patient Dataset (ILPD) style (583 records, 10 features), matching PPT literature survey references [3], [24] and Slide 28 Implementation.

**Input fields:**

| Field | Type | Example range/values |
|---|---|---|
| age | integer | 4–90 |
| gender | categorical | Male / Female |
| total bilirubin | float (mg/dl) | 0.4–75 |
| direct bilirubin | float (mg/dl) | 0.1–19.7 |
| alkaline phosphotase | integer (IU/L) | 63–2110 |
| alamine aminotransferase (SGPT) | integer (IU/L) | 10–2000 |
| aspartate aminotransferase (SGOT) | integer (IU/L) | 10–4929 |
| total proteins | float (g/dl) | 2.7–9.6 |
| albumin | float (g/dl) | 0.9–5.5 |
| albumin/globulin ratio | float | 0.3–2.8 |

**Validation:** numeric bounds as above; gender via dropdown.

**Prediction workflow:** encode, scale, predict, map to "Liver Disease Likely" / "Liver Disease Unlikely".

**Output format:** risk label, confidence %, disclaimer.

### 10.4 Lung Disease

**Reference dataset pattern:** Tabular lung-cancer risk survey dataset (lifestyle/symptom-based, e.g., the commonly used "Lung Cancer Dataset" with columns like smoking, yellow fingers, anxiety, chronic disease, fatigue, coughing, shortness of breath, swallowing difficulty, chest pain).

**Documented MVP approach (per Section 7.2):** structured/tabular, symptom-and-lifestyle-based classification — **not** CT-scan image analysis.

**Input fields:**

| Field | Type | Example range/values |
|---|---|---|
| age | integer | 18–100 |
| gender | categorical | Male / Female |
| smoking | boolean | Yes/No |
| yellow fingers | boolean | Yes/No |
| anxiety | boolean | Yes/No |
| peer pressure | boolean | Yes/No |
| chronic disease | boolean | Yes/No |
| fatigue | boolean | Yes/No |
| allergy | boolean | Yes/No |
| wheezing | boolean | Yes/No |
| alcohol consuming | boolean | Yes/No |
| coughing | boolean | Yes/No |
| shortness of breath | boolean | Yes/No |
| swallowing difficulty | boolean | Yes/No |
| chest pain | boolean | Yes/No |

**Validation:** all fields required; booleans via radio/toggle; age bounded.

**Prediction workflow:** encode, scale (if needed for the chosen model), predict, map to "Lung Disease Risk: High" / "Lung Disease Risk: Low".

**Output format:** risk label, confidence %, disclaimer, plus a one-line note clarifying this module is a symptom/lifestyle-based screening indicator, not an imaging-based diagnosis.

### 10.5 Breast Cancer

**Reference dataset pattern:** Wisconsin Diagnostic Breast Cancer (WDBC) dataset (30 numeric features derived from digitized fine needle aspirate images), matching PPT literature survey references [19], [20].

**Input fields:** the 10 core measurements (mean values) are sufficient for a usable MVP form; the coding agent may expose all 30 (mean/SE/worst for each) if time allows, but 10 mean-value fields are the MVP baseline:

| Field | Type | Example range/values |
|---|---|---|
| radius_mean | float | 6–30 |
| texture_mean | float | 9–40 |
| perimeter_mean | float | 40–190 |
| area_mean | float | 140–2500 |
| smoothness_mean | float | 0.05–0.16 |
| compactness_mean | float | 0.02–0.35 |
| concavity_mean | float | 0.0–0.43 |
| concave_points_mean | float | 0.0–0.20 |
| symmetry_mean | float | 0.1–0.30 |
| fractal_dimension_mean | float | 0.05–0.10 |

**Validation:** numeric bounds as above (all continuous, all required).

**Prediction workflow:** encode (none needed, all numeric), scale, predict, map to "Malignant" / "Benign".

**Output format:** result label (Malignant/Benign), confidence %, disclaimer — phrased carefully as a statistical estimate, not a pathology diagnosis.

---

## 11. Functional Requirements

1. **FR-1:** The system shall present a Home/Dashboard page listing all five diseases as navigable cards.
2. **FR-2:** The system shall allow the user to navigate to any of the five disease prediction pages from the dashboard or sidebar at any time.
3. **FR-3:** Each disease page shall present a form containing all clinical input fields defined in Section 10 for that disease.
4. **FR-4:** The system shall validate all inputs (type, range, required) before allowing prediction; invalid input shall produce an inline error message and block submission.
5. **FR-5:** On valid submission, the system shall preprocess the input (encode categoricals, scale numerics) using the same transformation fitted during training.
6. **FR-6:** The system shall load the pre-trained, serialized model for the selected disease and generate a prediction.
7. **FR-7:** The system shall display the prediction result as a clear label (e.g., risk category) plus a confidence/probability percentage wherever the model supports `predict_proba`.
8. **FR-8:** The system shall display a medical disclaimer on the dashboard, on every prediction page, and alongside every result.
9. **FR-9:** The system shall display basic model information per disease (algorithm used, and its measured accuracy/F1 from the last training run) accessible from each prediction page.
10. **FR-10:** The system shall handle missing model/artifact files gracefully, showing a clear in-app error rather than crashing (see Section 18).
11. **FR-11:** The system shall not require any internet connection, login, or external service call to produce a prediction once models are trained and saved locally.
12. **FR-12:** The system shall show a loading indicator (e.g., Streamlit spinner) during preprocessing + inference.
13. **FR-13:** The system shall visually distinguish a "positive/high-risk" result from a "negative/low-risk" result (e.g., color coding: red/orange for high risk, green for low risk).

---

## 12. Non-Functional Requirements

| Category | Requirement |
|---|---|
| **Performance** | A single prediction (preprocessing + inference) should complete in under 2 seconds on a standard laptop (matches PPT Hardware Requirements: i5, 8GB RAM). |
| **Reliability** | The app should not crash on malformed or edge-case input; all five modules should be independently testable and demoable without one disease's failure affecting another. |
| **Usability** | Forms should be grouped logically (e.g., vitals vs. lab values), labeled in plain language with units shown, and require no domain training to operate. |
| **Maintainability** | Modular code: one preprocessing module, one training script, and one prediction module per disease, all following the same pattern, so a new disease can be added by following the existing pattern. |
| **Scalability** | Architecture supports adding new diseases or swapping a better-performing model per disease without touching unrelated modules — this is an MVP-level scalability claim (code structure), not a claim about serving production traffic volumes. |
| **Security** | MVP-level only: no PII is persisted (predictions are stateless, nothing is written to disk or a database after inference); no authentication is implemented because there are no user accounts in the MVP. This is explicitly **not** HIPAA/production healthcare-grade security — see Section 23 (Risks and Limitations). |
| **Privacy** | Since no data is stored, there is no patient data retention to manage in the MVP. Any future addition of prediction history/database storage (Section 22) will require an explicit privacy and consent design pass. |

---

## 13. Machine Learning Pipeline

Applied identically, per disease, to keep the codebase consistent (`src/training/train_<disease>.py` for each of the five diseases):

1. **Dataset acquisition** — download/place the raw CSV for the disease into `datasets/raw/`.
2. **Dataset organization** — document source, feature list, and target column in `datasets/README.md`.
3. **Data cleaning** — drop unusable rows/columns (e.g., ID columns), standardize column names.
4. **Missing-value handling** — numeric: median imputation; categorical: mode imputation (or a documented dataset-specific rule if the dataset has a conventional approach, e.g., CKD's own missingness pattern).
5. **Categorical encoding** — label encoding or one-hot encoding as appropriate per feature; the exact encoder is fit on training data and serialized for reuse at inference time.
6. **Feature scaling** — `StandardScaler` (or `MinMaxScaler` for models sensitive to bounded ranges) fit on training data only, serialized for reuse at inference time.
7. **Feature selection** — start with all clinically meaningful features from Section 10; drop any with near-zero variance or that leak the target; document any drops.
8. **Train/test split** — 80/20 stratified split (stratify on target to preserve class balance), `random_state=42` for reproducibility.
9. **Model training** — train each of the candidate models listed in Section 14 for that disease on the training split.
10. **Model comparison** — evaluate all candidates on the held-out test split using the metrics in Section 13.1.
11. **Evaluation** — record accuracy, precision, recall, F1, ROC-AUC (binary classification tasks), and confusion matrix for every candidate.
12. **Best-model selection** — select the model with the best F1-score (preferred over raw accuracy, since medical datasets are often class-imbalanced) as the disease's production model; document the choice and metrics in `models/<disease>/metadata.json`.
13. **Model serialization** — save the winning model and its fitted preprocessing objects (scaler/encoder) with `joblib.dump()` into `models/<disease>/`.
14. **Integration with Streamlit** — the corresponding prediction page loads these serialized artifacts once (cached with `st.cache_resource`) and reuses them across requests.

### 13.1 Evaluation Metrics
Accuracy, Precision, Recall, F1-Score, ROC-AUC (where the target is binary and probabilities are available), and Confusion Matrix — matching PPT Slide 29 exactly.

---

## 14. Dataset Strategy

For each disease, the dataset type, expected features, and target are specified below. **No dataset URLs are fabricated.** The coding agent should source each dataset from a well-known public repository (UCI Machine Learning Repository or Kaggle are the standard homes for each of these five classic datasets) and verify the actual file/column names at download time, since exact filenames vary by source/mirror. If a listed dataset cannot be located, the fallback is to search for the nearest equivalent public tabular dataset for that disease with a comparable feature set, and document the substitution in `datasets/README.md`.

| Disease | Dataset type | Feature count | Target variable | Notes |
|---|---|---|---|---|
| Heart Disease | Tabular clinical (UCI Heart Disease-style) | ~13 | Presence of heart disease (binary/multiclass collapsed to binary) | Well-known, small, clean; fast to train. |
| Kidney Disease | Tabular clinical (Kaggle CKD-style) | ~24–25 | CKD / Not CKD | Cited directly in PPT literature survey [7] with 98% accuracy achieved. |
| Liver Disease | Tabular clinical (ILPD-style) | ~10 | Liver patient / Not liver patient | Cited directly in PPT literature survey [3] and Slide 28. |
| Lung Disease | Tabular symptom/lifestyle survey | ~15 | Lung cancer risk: Yes/No | MVP substitute for imaging-based approach — see Section 7.2. |
| Breast Cancer | Tabular diagnostic (WDBC-style) | 10 (mean features) up to 30 (full) | Malignant / Benign | Cited directly in PPT literature survey [19], [20]. |

**Dataset preparation requirements (applies to all five):**
- Store the raw, unmodified download in `datasets/raw/<disease>.csv`.
- Store the cleaned, feature-engineered version in `datasets/processed/<disease>_clean.csv`.
- Record row count, feature list, target distribution, and any imputation/encoding decisions in `datasets/README.md`.
- Never commit personally identifiable patient data — these are all de-identified public research datasets, which is a hard requirement for using them in this project.

---

## 15. Model Training and Evaluation

### 15.1 Candidate Models Per Disease
All five diseases use the same candidate pool (as in the PPT's Section 4.2 and Slide 24), with the best performer per disease selected empirically:

- Logistic Regression
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
- Gradient Boosting

**XGBoost** may optionally be added per disease if it is already available in the environment (`pip install xgboost`) and its accuracy/F1 clearly beats the sklearn candidates above; it is not required, since the PPT's own literature survey shows sklearn's Random Forest/Gradient Boosting reaching comparable (95–99%) accuracy without the extra dependency. **CNN is intentionally excluded from the MVP model pool** for all five diseases, consistent with the tabular-data decision in Section 7.2.

### 15.2 Selection Rule
For each disease: train all candidate models on the same train split → evaluate all on the same test split → select the model with the highest F1-score (ties broken by ROC-AUC, then accuracy) → serialize that model as the disease's production model.

### 15.3 Reporting
For every disease, `models/<disease>/metadata.json` must record: model type chosen, all metrics for the chosen model, and (for comparison) the metric table for every candidate that was tried. This file is what powers the "Model Information" panel in the UI (FR-9) and what the team will screenshot for the demonstration (Section 20, step 8).

---

## 16. User Interface Requirements

### 16.1 Navigation Structure
- **Sidebar:** persistent across all pages, listing "Home" plus all five diseases, using Streamlit's native multi-page navigation (`pages/1_Heart_Disease.py`, `pages/2_Kidney_Disease.py`, etc. — numeric prefixes control sidebar order).
- **Home page (`app.py`):** landing page, does not require any input to view.

### 16.2 Home/Dashboard Requirements
- Project title and one-paragraph description (adapted from PPT Slide 3 Overview).
- Five disease cards (icon/emoji + disease name + one-line description + "Go to prediction" action), matching the emoji cues already used in the project brief (❤️ Heart, 🫘 Kidney, 🫀 Liver, 🫁 Lung, 🎗️ Breast Cancer).
- "System overview" section: how the app works (enter details → data processed → model predicts → result shown), matching PPT Slide 24.
- "Technologies used" section listing the stack from Section 9.
- Medical disclaimer, clearly visible without scrolling on a standard screen.

### 16.3 Disease Page Requirements
- Page title and short description of what the module predicts.
- Form fields grouped logically (e.g., "Vitals," "Lab Values," "Symptoms" — grouping varies per disease per Section 10).
- Clear units shown next to every numeric field.
- A single "Predict" button, disabled/greyed out until required fields are filled or containing sensible defaults so it's always clickable but validated on submit.
- A loading state (Streamlit spinner) while inference runs.
- A result card that visually differs for positive/negative predictions (e.g., red-tinted card with a warning icon for high risk, green-tinted card with a check icon for low risk), containing: prediction label, confidence %, and a one-line reminder that this is not a medical diagnosis.
- A collapsible "Model Info" section (algorithm name + accuracy/F1 from the last training run, pulled from that disease's `metadata.json`).
- Disclaimer text repeated at the bottom of the results.

### 16.4 Visual Design Direction
- Healthcare-appropriate palette (clean whites/blues/teals; avoid alarmist reds except for the high-risk result state).
- Consistent card-based layout across the dashboard and all five prediction pages.
- Responsive within Streamlit's layout system (`st.columns` for grouping fields side by side on wide screens).

---

## 17. Project Folder Structure

```
multi-disease-prediction-system/
│
├── app.py                          # Home/Dashboard page (Streamlit entry point)
├── pages/
│   ├── 1_Heart_Disease.py
│   ├── 2_Kidney_Disease.py
│   ├── 3_Liver_Disease.py
│   ├── 4_Lung_Disease.py
│   └── 5_Breast_Cancer.py
│
├── src/
│   ├── preprocessing/
│   │   ├── heart_preprocessing.py
│   │   ├── kidney_preprocessing.py
│   │   ├── liver_preprocessing.py
│   │   ├── lung_preprocessing.py
│   │   └── breast_cancer_preprocessing.py
│   ├── training/
│   │   ├── train_heart.py
│   │   ├── train_kidney.py
│   │   ├── train_liver.py
│   │   ├── train_lung.py
│   │   └── train_breast_cancer.py
│   ├── prediction/
│   │   └── predict.py              # shared load-model + predict helper, parameterized by disease
│   └── utils/
│       ├── validation.py           # shared input-range validation helpers
│       └── constants.py            # shared field ranges, labels, disclaimer text
│
├── models/
│   ├── heart/          (model.pkl, scaler.pkl, metadata.json)
│   ├── kidney/          (model.pkl, scaler.pkl, encoder.pkl, metadata.json)
│   ├── liver/           (model.pkl, scaler.pkl, encoder.pkl, metadata.json)
│   ├── lung/            (model.pkl, scaler.pkl, metadata.json)
│   └── breast_cancer/   (model.pkl, scaler.pkl, metadata.json)
│
├── datasets/
│   ├── raw/              (5x original CSVs)
│   ├── processed/        (5x cleaned CSVs)
│   └── README.md          (source, features, target, prep notes per dataset)
│
├── assets/
│   └── images/            (disease icons, logo, screenshots for report)
│
├── requirements.txt
├── README.md               # setup + run instructions
└── PRD.md                    # this document
```

This structure directly matches the PPT's proposed layout (Slide/brief mentions `app.py`, `pages/`, `models/`, `datasets/`, `src/{preprocessing,training,prediction}/`, `assets/`), with the addition of a small `src/utils/` module for shared validation/constants — necessary so five near-identical pages don't duplicate range-checking and label logic.

---

## 18. Error Handling

| Failure case | Required behavior |
|---|---|
| Missing model file (`model.pkl` not found) | Show an in-app `st.error()` message: "Model for [Disease] is not available. Please contact the development team." Do not crash the whole app — other disease pages must remain usable. |
| Missing dataset file at training time | Training script exits with a clear message naming the expected path and instructing the user to place the dataset there; does not silently generate fake data. |
| Invalid numeric input (non-numeric text typed into a numeric field) | Streamlit's native numeric input widgets prevent this at the widget level; additionally validate server-side before prediction. |
| Out-of-range value | Inline warning under the field ("Value must be between X and Y") and Predict button disabled until corrected. |
| Model loading error (corrupted pickle, version mismatch) | Catch the exception, show `st.error()` with a generic "Unable to load the prediction model" message, log the actual exception to console/log file for debugging. |
| Prediction failure (unexpected exception in `model.predict()`) | Catch, show a generic error to the user, log details for developers; never show a raw traceback in the UI. |
| Missing dependencies (e.g., `xgboost` not installed but referenced) | `requirements.txt` must pin every library actually imported; app should fail fast with a clear `ModuleNotFoundError`-derived message during startup checks, not deep inside a prediction call. |

---

## 19. Testing Strategy

### 19.1 Functional Testing
- Navigation: every sidebar link loads the correct page without error.
- Disease selection: dashboard cards route to the correct prediction page.
- Form validation: submitting with missing/invalid/out-of-range values is blocked with a clear message; submitting valid values succeeds.
- Prediction functionality: for each disease, submit at least one known "likely low risk" and one known "likely high risk" set of sample values (drawn from real dataset rows) and confirm the result direction is sensible.
- Result display: confidence percentage renders, label renders, disclaimer renders, color coding matches the predicted class.

### 19.2 Machine Learning Testing
- Dataset preprocessing: unit-check that the saved scaler/encoder produces the same transformation on a known sample row every time (determinism check).
- Model training: training script runs end-to-end without error and produces all expected artifact files.
- Evaluation metrics: accuracy/precision/recall/F1/ROC-AUC computed and logged for every candidate model per disease.
- Confusion matrix: generated and saved (as an image or in `metadata.json`) for the final chosen model per disease.
- Unseen test data: all reported metrics come from the held-out 20% test split, never from data the model was trained on.

---

## 20. Demonstration Workflow

Directly adapted from PPT Slide 30, sequenced for a live college evaluation:

1. Open the application (`streamlit run app.py`) and show the Home/Dashboard.
2. Explain the dashboard: project purpose, the five diseases covered, tech stack.
3. Select a disease (e.g., Heart Disease) from the sidebar/card.
4. Enter a realistic sample set of medical parameter values (prepared in advance from the test dataset).
5. Click Predict and show the result: label + confidence.
6. Briefly explain which ML model produced this result and why it was chosen (via the Model Info panel).
7. Repeat steps 3–6 quickly for the remaining four diseases.
8. Show the model evaluation results (accuracy/precision/recall/F1/confusion matrix) prepared beforehand, either in the app's Model Info panels or in a short results slide/notebook output.
9. Close with a one-line reminder of the medical disclaimer and a mention of future scope (imaging-based CNN modules, IoT, etc.).

---

## 21. MVP Acceptance Criteria

The project is considered demo-ready when **all** of the following are true:

- [ ] All five disease datasets are downloaded, cleaned, and documented in `datasets/README.md`.
- [ ] All five training scripts run successfully and produce a serialized model + preprocessing artifacts + `metadata.json` per disease.
- [ ] Every disease's chosen model has measured accuracy, precision, recall, and F1-score recorded (no invented numbers).
- [ ] The Streamlit app launches locally with a single command and shows a working Home/Dashboard.
- [ ] All five prediction pages accept input, validate it, run inference, and display a labeled result with confidence.
- [ ] Medical disclaimers appear on the dashboard and on every result.
- [ ] The app does not crash on any of the error cases listed in Section 18 (verified by manual testing).
- [ ] The full demonstration workflow (Section 20) can be run start-to-finish in under 10 minutes without errors.

---

## 22. Future Enhancements

Explicitly preserved from the PPT as documented, non-MVP future scope — not built now, but not discarded from the project's vision:

- **Medical image analysis (CNN):** CT scans for lung disease, mammography images for breast cancer, using architectures referenced in the literature survey (CNN, ResNet, InceptionV3).
- **Genetic-data-based prediction:** incorporating genetic markers for lung disease risk, as explored in literature survey reference [2].
- **IoT / wearable device integration:** real-time heart-rate/ECG monitoring feeding into the Heart Disease module, as explored in literature survey reference [10].
- **Cloud deployment:** hosting the app (e.g., Streamlit Community Cloud, AWS, Azure) for remote access beyond the local demo.
- **Database + prediction history:** persisting past predictions per (authenticated) user for longitudinal tracking.
- **User authentication:** patient and clinician accounts with role-based access.
- **Doctor dashboard:** an aggregate view across multiple patients for clinicians.
- **Explainable AI (SHAP/LIME):** feature-importance visualizations per prediction, as used in literature survey references [3] and [24].
- **Multi-language support:** for broader accessibility, especially in the "resource-limited settings" use case named in the PPT's societal scope.

---

## 23. Risks and Limitations

- **Data size and generalizability:** several of the reference datasets (e.g., 583-row ILPD, 1025-row heart dataset) are small by modern ML standards; reported accuracy may not generalize to a broader real-world population. This must be stated plainly in the demo and report, not hidden behind a high accuracy number.
- **Not a certified medical device:** this system is a machine-learning-based prediction/decision-support **prototype** built for academic demonstration. It has not been clinically validated, is not regulatory-approved, and must never be presented or used as a substitute for professional medical diagnosis.
- **Class imbalance:** some target classes (e.g., CKD-positive vs. CKD-negative) may be imbalanced; F1-score is prioritized over raw accuracy for this reason (Section 15.2), and the confusion matrix must always be reviewed alongside the headline metric.
- **Lung Disease module scope change:** the literature survey and parts of the PPT reference CT-scan/genetic approaches to lung disease; this PRD deliberately substitutes a tabular symptom/lifestyle-survey approach for the MVP (Section 7.2/10.4). This is a documented, deliberate scope decision, not an oversight, and should be explained as such in the final report and viva.
- **Security is MVP-level only:** no encryption at rest, no authentication, no audit logging — acceptable for a local academic demo, explicitly not acceptable for handling real patient data in production (Section 12).
- **Single point of truth for "confidence":** the displayed confidence is the model's own `predict_proba()` output, which is a statistical estimate, not a calibrated clinical probability; this distinction should be verbally acknowledged during the demo.

---

## 24. Medical Disclaimer

> **Medical Disclaimer:** This Multi-Disease Prediction System is an academic machine-learning prototype developed for educational and demonstration purposes as part of a college major project. It is **not** a certified medical device, and its predictions are **not** a substitute for professional medical diagnosis, advice, or treatment. Predictions are statistical estimates generated from limited public datasets and general clinical parameters; they do not account for a user's full medical history and may be inaccurate. Always consult a qualified healthcare professional for any medical concern. The developers and the institution accept no liability for decisions made based on this system's output.

This exact disclaimer (or a lightly reworded equivalent preserving all of the above points) must appear on the Home/Dashboard page, on every disease prediction page, and alongside every displayed result, per FR-8.

---

## 25. Development Roadmap

Suggested sequencing for the AI coding agent (and for the team, if built manually), designed so a working end-to-end slice exists as early as possible:

**Phase 1 — Foundation**
1. Set up folder structure (Section 17), `requirements.txt`, and a minimal `app.py` that just renders the dashboard shell.
2. Build `src/utils/constants.py` and `src/utils/validation.py` (shared field ranges, disclaimer text, label maps) so every disease module can reuse them.

**Phase 2 — First Vertical Slice (proves the architecture)**
3. Acquire, clean, and document the Breast Cancer dataset (simplest: fully numeric, no encoding needed).
4. Build `train_breast_cancer.py`, run it, produce `models/breast_cancer/`.
5. Build `pages/5_Breast_Cancer.py` end-to-end (form → validate → preprocess → predict → display).
6. Confirm this one module works fully in the running Streamlit app before moving on — this is the template every other disease module copies.

**Phase 3 — Remaining Disease Modules**
7. Repeat the acquire → clean → train → build-page pattern for Heart Disease, then Liver Disease, then Kidney Disease, then Lung Disease, reusing the Breast Cancer module's code structure each time.

**Phase 4 — Polish and Integration**
8. Build out the full Home/Dashboard (cards, tech stack section, disclaimer).
9. Apply consistent visual styling across all five pages (Section 16.4).
10. Add the Model Info panel (reading each disease's `metadata.json`) to every page.
11. Implement all error-handling cases from Section 18.

**Phase 5 — Testing and Demo Prep**
12. Run through the full functional and ML testing checklist (Section 19).
13. Verify every MVP Acceptance Criterion (Section 21).
14. Prepare sample input values for the demo (Section 20) using real rows from each test dataset.
15. Do a full dry-run of the demonstration workflow, timed, before the actual evaluation.

---

*End of PRD. This document is the master blueprint; any implementation decision not covered here should follow the same priorities used throughout: fast, reliable, honestly-reported, and faithful to the original five-disease, tabular-ML, Streamlit-based project concept from the source PowerPoint.*
