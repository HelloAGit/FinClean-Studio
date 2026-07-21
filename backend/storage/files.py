import os
import pandas as pd
from fastapi import UploadFile

BASE_DIR = "storage"
SOURCE_DIR = os.path.join(BASE_DIR, "source")
CLEANED_DIR = os.path.join(BASE_DIR, "cleaned")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

for d in [SOURCE_DIR, CLEANED_DIR, REPORT_DIR]:
    os.makedirs(d, exist_ok=True)

def save_source_file(file: UploadFile) -> str:
    path = os.path.join(SOURCE_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(await file.read())  # if you keep async, adjust signature
    return path

def load_dataset(path_or_id: str) -> pd.DataFrame:
    # MVP: treat path_or_id as path
    if path_or_id.endswith(".xlsx") or path_or_id.endswith(".xls"):
        return pd.read_excel(path_or_id)
    return pd.read_csv(path_or_id)

def save_cleaned_dataset(dataset_id: str, df: pd.DataFrame, version: str) -> str:
    filename = f"{dataset_id}_{version}_cleaned.csv"
    path = os.path.join(CLEANED_DIR, filename)
    df.to_csv(path, index=False)
    return path

def save_report_file(job_id: str, name: str, df_or_content) -> str:
    path = os.path.join(REPORT_DIR, f"{job_id}_{name}")
    if isinstance(df_or_content, pd.DataFrame):
        if name.endswith(".csv"):
            df_or_content.to_csv(path, index=False)
        else:
            df_or_content.to_json(path, orient="records")
    else:
        with open(path, "w") as f:
            f.write(str(df_or_content))
    return path
