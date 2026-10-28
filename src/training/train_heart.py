"""
Training script for Heart Disease Prediction model.
Trains 6 candidate algorithms, evaluates on held-out test split,
selects the best model by F1-score, and exports model artifacts + metadata.
"""
import os
import json
import datetime
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_PATH = os.path.join(BASE_DIR, "datasets", "raw", "heart.csv")
CLEAN_PATH = os.path.join(BASE_DIR, "datasets", "processed", "heart_clean.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models", "heart")
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "datasets", "processed"), exist_ok=True)

def train_heart_model():
    print("=" * 60)
    print(" TRAINING HEART DISEASE PREDICTION MODEL ")
    print("=" * 60)

    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"Raw heart dataset not found at {RAW_PATH}")

    df = pd.read_csv(RAW_PATH)
    print(f"Loaded raw dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    # Standardize target: in raw Kaggle heart.csv, 0 is disease and 1 is healthy.
    # We standardize so that 1 = Heart Disease Present (High Risk) and 0 = Healthy (Low Risk)
    # Check if target=0 has higher oldpeak than target=1
    if df[df["target"] == 0]["oldpeak"].mean() > df[df["target"] == 1]["oldpeak"].mean():
        print("Standardizing target: flipping 0 (disease) -> 1, 1 (healthy) -> 0")
        df["target"] = 1 - df["target"]

    # Clean dataset: handle any missing values
    df = df.dropna()
    df.to_csv(CLEAN_PATH, index=False)
    print(f"Saved cleaned dataset to {CLEAN_PATH}")

    feature_cols = [c for c in df.columns if c != "target"]
    X = df[feature_cols]
    y = df["target"]

    # Stratified 80/20 train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    candidates = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42),
        "Support Vector Machine": SVC(probability=True, kernel="rbf", random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    }

    results = {}
    pipelines = {}

    print("\nEvaluating Candidate Models:")
    print("-" * 60)

    for name, clf in candidates.items():
        pipe = Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", clf)
        ])
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        y_proba = pipe.predict_proba(X_test)[:, 1] if hasattr(pipe.named_steps["classifier"], "predict_proba") else None

        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, zero_division=0))
        rec = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))
        roc = float(roc_auc_score(y_test, y_proba)) if y_proba is not None else 0.0
        cm = confusion_matrix(y_test, y_pred).tolist()

        results[name] = {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc, 4),
            "confusion_matrix": cm
        }
        pipelines[name] = pipe

        print(f"[{name}] Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | ROC-AUC: {roc:.4f}")

    # Select best model by F1-score (tie-breaker: ROC-AUC, then accuracy)
    best_name = max(results.keys(), key=lambda k: (results[k]["f1_score"], results[k]["roc_auc"], results[k]["accuracy"]))
    best_pipe = pipelines[best_name]
    best_metrics = results[best_name]

    print("\n" + "=" * 60)
    print(f" SELECTED BEST MODEL: {best_name}")
    print(f" F1-Score: {best_metrics['f1_score']} | Accuracy: {best_metrics['accuracy']} | ROC-AUC: {best_metrics['roc_auc']}")
    print("=" * 60)

    # Serialize best pipeline
    model_path = os.path.join(MODEL_DIR, "model.pkl")
    joblib.dump(best_pipe, model_path)
    print(f"Saved trained pipeline to {model_path}")

    # Export metadata
    metadata = {
        "disease": "Heart Disease",
        "model_name": best_name,
        "accuracy": best_metrics["accuracy"],
        "precision": best_metrics["precision"],
        "recall": best_metrics["recall"],
        "f1_score": best_metrics["f1_score"],
        "roc_auc": best_metrics["roc_auc"],
        "confusion_matrix": best_metrics["confusion_matrix"],
        "feature_names": feature_cols,
        "dataset_rows": len(df),
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "candidate_comparison": results,
        "last_trained": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    meta_path = os.path.join(MODEL_DIR, "metadata.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Saved metadata to {meta_path}")

    return metadata

if __name__ == "__main__":
    train_heart_model()
