import os
import requests
import pandas as pd
from sklearn.datasets import load_breast_cancer

RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "datasets", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

DATASET_URLS = {
    "heart": [
        # (bundled dataset is used; no external download URLs)
    ],
    "kidney": [
        # (bundled dataset is used; no external download URLs)
    ],
    "liver": [
        # (bundled dataset is used; no external download URLs)
    ],
    "lung": [
        # (bundled dataset is used; no external download URLs)
    ]
}

def download_file(urls, dest_path):
    for url in urls:
        try:
            print(f"Attempting download from: {url}")
            r = requests.get(url, timeout=15)
            if r.status_code == 200 and len(r.content) > 100:
                with open(dest_path, "wb") as f:
                    f.write(r.content)
                print(f"Successfully downloaded to {dest_path} ({len(r.content)} bytes)")
                return True
        except Exception as e:
            print(f"Failed {url}: {e}")
    return False

def acquire_all():
    # 1. Breast Cancer
    bc_path = os.path.join(RAW_DIR, "breast_cancer.csv")
    if not os.path.exists(bc_path):
        print("Loading Breast Cancer dataset from scikit-learn...")
        bc = load_breast_cancer(as_frame=True)
        df_bc = bc.frame
        # Rename target column to diagnosis (1: Benign, 0: Malignant in sklearn, but let's check standard)
        # In sklearn: 0 = 'malignant', 1 = 'benign'. Let's save target as 'target' or 'diagnosis'
        df_bc.to_csv(bc_path, index=False)
        print(f"Saved breast cancer dataset: {df_bc.shape}")
    else:
        print(f"Breast cancer dataset already exists at {bc_path}")

    # 2. Heart
    heart_path = os.path.join(RAW_DIR, "heart.csv")
    if not os.path.exists(heart_path):
        success = download_file(DATASET_URLS["heart"], heart_path)
        if not success:
            print("ERROR: Could not download Heart dataset!")
    else:
        print(f"Heart dataset already exists at {heart_path}")

    # 3. Kidney
    kidney_path = os.path.join(RAW_DIR, "kidney.csv")
    if not os.path.exists(kidney_path):
        success = download_file(DATASET_URLS["kidney"], kidney_path)
        if not success:
            print("ERROR: Could not download Kidney dataset!")
    else:
        print(f"Kidney dataset already exists at {kidney_path}")

    # 4. Liver
    liver_path = os.path.join(RAW_DIR, "liver.csv")
    if not os.path.exists(liver_path):
        success = download_file(DATASET_URLS["liver"], liver_path)
        if not success:
            print("ERROR: Could not download Liver dataset!")
    else:
        print(f"Liver dataset already exists at {liver_path}")

    # 5. Lung
    lung_path = os.path.join(RAW_DIR, "lung.csv")
    if not os.path.exists(lung_path):
        success = download_file(DATASET_URLS["lung"], lung_path)
        if not success:
            print("ERROR: Could not download Lung dataset!")
    else:
        print(f"Lung dataset already exists at {lung_path}")

if __name__ == "__main__":
    acquire_all()
