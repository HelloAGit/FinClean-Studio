import json
import pandas as pd
from typing import List
from models import AuditRecord
from storage.files import save_report_file
import uuid

def build_reconciliation_summary(df: pd.DataFrame) -> dict:
    # Simple GL-style reconciliation: debit vs credit totals if present
    summary = {}
    if "debit" in df.columns and "credit" in df.columns:
        debit = pd.to_numeric(df["debit"], errors="coerce").sum()
        credit = pd.to_numeric(df["credit"], errors="coerce").sum()
        summary["debit_total"] = float(debit)
        summary["credit_total"] = float(credit)
        summary["balanced"] = abs(debit - credit) < 1e-6
    return summary

def export_job(dataset_id: str, cleaned_df: pd.DataFrame, audit_log: List[AuditRecord]):
    job_id = str(uuid.uuid4())

    # Cleaned file
    cleaned_path = save_report_file(job_id, "cleaned.csv", cleaned_df)

    # Rejected records (MVP: rows with any missing required fields)
    rejected_df = cleaned_df[cleaned_df.isna().any(axis=1)]
    rejected_path = save_report_file(job_id, "rejected.csv", rejected_df)

    # Audit log
    audit_path = save_report_file(job_id, "audit_log.json", pd.DataFrame([a.dict() for a in audit_log]))

    # Data-quality report (simple JSON)
    reconciliation = build_reconciliation_summary(cleaned_df)
    dq_report = {
        "dataset_id": dataset_id,
        "job_id": job_id,
        "reconciliation": reconciliation,
        "record_count": int(len(cleaned_df)),
    }
    dq_report_path = save_report_file(job_id, "data_quality_report.json", pd.DataFrame([dq_report]))

    # Machine-readable cleaning recipe (rules + decisions)
    recipe = {
        "dataset_id": dataset_id,
        "job_id": job_id,
        "steps": [
            # MVP: high-level description; later: full transformation graph
            "profile_dataset",
            "apply_rules",
            "review_corrections",
            "export_cleaned_dataset",
        ],
    }
    recipe_path = save_report_file(job_id, "cleaning_recipe.json", pd.DataFrame([recipe]))

    return {
        "job_id": job_id,
        "artefacts": {
            "cleaned_file": cleaned_path,
            "rejected_records": rejected_path,
            "audit_log": audit_path,
            "data_quality_report": dq_report_path,
            "cleaning_recipe": recipe_path,
        },
    }

def get_job_summary(job_id: str):
    # MVP: return paths only; could be extended to signed URLs
    return {
        "job_id": job_id,
        "message": "Job completed. Artefacts available on disk.",
    }
