# Datasets Documentation — Multi-Disease Prediction System

This directory contains the raw and cleaned datasets used for training machine learning models for the five disease prediction modules.

All datasets are publicly available, de-identified clinical and epidemiological benchmark datasets suitable for academic and research use.

---

## 1. Heart Disease Dataset

* **Raw File:** `datasets/raw/heart.csv`
* **Cleaned File:** `datasets/processed/heart_clean.csv`
* **Source:** UCI Machine Learning Repository (Cleveland Heart Disease Database)
* **Number of Rows:** 303
* **Number of Features:** 13 clinical attributes + 1 target
* **Target Variable:** `target` (1 = Presence of heart disease / High Risk, 0 = Absence / Low Risk)
* **Features:**
  1. `age`: Age in years (18–100)
  2. `sex`: Sex (1 = Male, 0 = Female)
  3. `cp`: Chest pain type (0 = Typical angina, 1 = Atypical angina, 2 = Non-anginal pain, 3 = Asymptomatic)
  4. `trestbps`: Resting blood pressure (in mm Hg on admission to the hospital, 80–200)
  5. `chol`: Serum cholesterol in mg/dl (100–600)
  6. `fbs`: Fasting blood sugar > 120 mg/dl (1 = True, 0 = False)
  7. `restecg`: Resting electrocardiographic results (0 = Normal, 1 = ST-T wave abnormality, 2 = Left ventricular hypertrophy)
  8. `thalach`: Maximum heart rate achieved (60–220 bpm)
  9. `exang`: Exercise-induced angina (1 = Yes, 0 = No)
  10. `oldpeak`: ST depression induced by exercise relative to rest (0.0–6.5)
  11. `slope`: Slope of the peak exercise ST segment (0 = Upsloping, 1 = Flat, 2 = Downsloping)
  12. `ca`: Number of major vessels (0–4) colored by fluoroscopy
  13. `thal`: Thalassemia (1 = Normal, 2 = Fixed defect, 3 = Reversible defect)
* **Preprocessing:** Handled missing values, numerical scaling via StandardScaler, stratified train-test split (80/20).

---

## 2. Chronic Kidney Disease (CKD) Dataset

* **Raw File:** `datasets/raw/kidney.csv`
* **Cleaned File:** `datasets/processed/kidney_clean.csv`
* **Source:** UCI Machine Learning Repository (Chronic Kidney Disease Dataset, ID: 336)
* **Number of Rows:** 400
* **Number of Features:** 24 clinical attributes + 1 target
* **Target Variable:** `class` (1 = `ckd` / Kidney Disease Likely, 0 = `notckd` / Kidney Disease Unlikely)
* **Features:**
  1. `age`: Age in years (1–100)
  2. `bp`: Blood pressure (in mm Hg, 50–180)
  3. `sg`: Specific gravity (1.005, 1.010, 1.015, 1.020, 1.025)
  4. `al`: Albumin level (0–5)
  5. `su`: Sugar level (0–5)
  6. `rbc`: Red blood cells (normal / abnormal)
  7. `pc`: Pus cell (normal / abnormal)
  8. `pcc`: Pus cell clumps (present / notpresent)
  9. `ba`: Bacteria (present / notpresent)
  10. `bgr`: Blood glucose random (mg/dl, 22–500)
  11. `bu`: Blood urea (mg/dl, 1.5–400)
  12. `sc`: Serum creatinine (mg/dl, 0.4–76)
  13. `sod`: Sodium (mEq/L, 4.5–163)
  14. `pot`: Potassium (mEq/L, 2.5–47)
  15. `hemo`: Hemoglobin (g/dl, 3.1–17.8)
  16. `pcv`: Packed cell volume (9–54)
  17. `wbcc`: White blood cell count (cells/cumm, 2200–26400)
  18. `rbcc`: Red blood cell count (millions/cmm, 2.1–8.0)
  19. `htn`: Hypertension (yes / no)
  20. `dm`: Diabetes mellitus (yes / no)
  21. `cad`: Coronary artery disease (yes / no)
  22. `appet`: Appetite (good / poor)
  23. `pe`: Pedal edema (yes / no)
  24. `ane`: Anemia (yes / no)
* **Preprocessing:** Stripped whitespace/tab formatting inconsistencies, median imputation for numerical features, mode imputation for categorical features, categorical encoding, standard scaling, stratified split (80/20).

---

## 3. Indian Liver Patient Dataset (ILPD)

* **Raw File:** `datasets/raw/liver.csv`
* **Cleaned File:** `datasets/processed/liver_clean.csv`
* **Source:** UCI Machine Learning Repository (ILPD, ID: 225)
* **Number of Rows:** 583
* **Number of Features:** 10 diagnostic attributes + 1 target
* **Target Variable:** `Selector` (1 = Liver Patient / High Risk, 0 = Non-Liver Patient / Low Risk; mapped from original 1=Patient, 2=Non-Patient)
* **Features:**
  1. `Age`: Age of the patient (4–90)
  2. `Gender`: Gender (Male / Female)
  3. `TB`: Total Bilirubin (mg/dl, 0.4–75.0)
  4. `DB`: Direct Bilirubin (mg/dl, 0.1–19.7)
  5. `Alkphos`: Alkaline Phosphotase (IU/L, 63–2110)
  6. `Sgpt`: Alamine Aminotransferase (IU/L, 10–2000)
  7. `Sgot`: Aspartate Aminotransferase (IU/L, 10–4929)
  8. `TP`: Total Proteins (g/dl, 2.7–9.6)
  9. `ALB`: Albumin (g/dl, 0.9–5.5)
  10. `A/G Ratio`: Albumin and Globulin Ratio (0.3–2.8)
* **Preprocessing:** Handled missing values in `A/G Ratio` via median imputation, mapped gender to binary indicator (1=Male, 0=Female), mapped target selector (1 -> 1, 2 -> 0), numerical standard scaling, stratified train-test split (80/20).

---

## 4. Lung Cancer Survey Dataset

* **Raw File:** `datasets/raw/lung.csv`
* **Cleaned File:** `datasets/processed/lung_clean.csv`
* **Source:** Kaggle / Survey Lung Cancer Dataset (derived from clinical survey research)
* **Number of Rows:** 276 unique patient survey records (deduplicated from raw survey collection to prevent train/test data leakage)
* **Number of Features:** 15 lifestyle/symptom attributes + 1 target
* **Target Variable:** `LUNG_CANCER` (1 = High Risk / Cancer Present, 0 = Low Risk / Negative)
* **Features:**
  1. `GENDER`: Gender (1 = Male, 0 = Female)
  2. `AGE`: Age in years (18–100)
  3. `SMOKING`: Smoking habit (1 = No, 2 = Yes)
  4. `YELLOW_FINGERS`: Yellow fingers (1 = No, 2 = Yes)
  5. `ANXIETY`: Anxiety (1 = No, 2 = Yes)
  6. `PEER_PRESSURE`: Peer pressure (1 = No, 2 = Yes)
  7. `CHRONIC_DISEASE`: Chronic disease history (1 = No, 2 = Yes)
  8. `FATIGUE`: Fatigue (1 = No, 2 = Yes)
  9. `ALLERGY`: Allergies (1 = No, 2 = Yes)
  10. `WHEEZING`: Wheezing (1 = No, 2 = Yes)
  11. `ALCOHOL_CONSUMING`: Alcohol consumption (1 = No, 2 = Yes)
  12. `COUGHING`: Persistent coughing (1 = No, 2 = Yes)
  13. `SHORTNESS_OF_BREATH`: Shortness of breath (1 = No, 2 = Yes)
  14. `SWALLOWING_DIFFICULTY`: Swallowing difficulty (1 = No, 2 = Yes)
  15. `CHEST_PAIN`: Chest pain (1 = No, 2 = Yes)
* **Preprocessing:** Standardized column naming, mapped categorical string indicators, deduplicated records prior to train/test split to eliminate duplicate contamination, applied StandardScaler within pipeline, stratified train-test split (80/20).

---

## 5. Wisconsin Diagnostic Breast Cancer (WDBC) Dataset

* **Raw File:** `datasets/raw/breast_cancer.csv`
* **Cleaned File:** `datasets/processed/breast_cancer_clean.csv`
* **Source:** Scikit-learn datasets / UCI Machine Learning Repository (WDBC)
* **Number of Rows:** 569
* **Number of Features:** 30 continuous numerical features (or 10 mean features in the focused core model) + 1 target
* **Target Variable:** `target` (1 = Malignant / High Risk, 0 = Benign / Low Risk)
* **Core 10 Mean Diagnostic Features:**
  1. `mean radius`: Mean of distances from center to points on the perimeter (6.0–30.0)
  2. `mean texture`: Standard deviation of gray-scale values (9.0–40.0)
  3. `mean perimeter`: Mean perimeter of the cell nucleus (40.0–190.0)
  4. `mean area`: Mean area of the cell nucleus (140.0–2500.0)
  5. `mean smoothness`: Mean of local variation in radius lengths (0.05–0.16)
  6. `mean compactness`: Mean of perimeter^2 / area - 1.0 (0.02–0.35)
  7. `mean concavity`: Mean of severity of concave portions of the contour (0.0–0.45)
  8. `mean concave points`: Mean for number of concave portions of the contour (0.0–0.20)
  9. `mean symmetry`: Mean symmetry score (0.10–0.30)
  10. `mean fractal dimension`: Mean for "coastline approximation" - 1 (0.05–0.10)
* **Preprocessing:** Extracted core diagnostic measurements, verified continuous distributions, applied StandardScaler, stratified train-test split (80/20).
