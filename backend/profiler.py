import pandas as pd
from pydantic import BaseModel
import uuid

class DatasetProfile(BaseModel):
    dataset_id: str
    rows: int
    columns: int
    data_types: dict
    missing_percentages: dict
    unique_counts: dict
    duplicate_rows: int
    amount_stats: dict
    date_ranges: dict
    currency_formats: dict
    sensitive_columns: list
    quality_score: float

def profile_dataset(df: pd.DataFrame) -> DatasetProfile:
    dataset_id = str(uuid.uuid4())
    rows, columns = df.shape

    data_types = df.dtypes.astype(str).to_dict()
    missing_percentages = (df.isna().mean() * 100).round(2).to_dict()
    unique_counts = df.nunique().to_dict()
    duplicate_rows = int(df.duplicated().sum())

    # Simple heuristic for amount columns
    amount_cols = [c for c in df.columns if "amount" in c.lower() or "value" in c.lower()]
    amount_stats = {}
    for col in amount_cols:
        numeric = pd.to_numeric(df[col], errors="coerce")
        amount_stats[col] = {
            "min": float(numeric.min()) if not numeric.empty else None,
            "max": float(numeric.max()) if not numeric.empty else None,
            "mean": float(numeric.mean()) if not numeric.empty else None,
        }

    # Simple heuristic for date columns
    date_cols = [c for c in df.columns if "date" in c.lower()]
    date_ranges = {}
    for col in date_cols:
        parsed = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
        date_ranges[col] = {
            "min": parsed.min().isoformat() if not parsed.isna().all() else None,
            "max": parsed.max().isoformat() if not parsed.isna().all() else None,
        }

    # Currency formats (very basic MVP)
    currency_formats = {}
    for col in amount_cols:
        sample = df[col].dropna().astype(str).head(50)
        currency_formats[col] = {
            "examples": sample.tolist(),
        }

    # Potentially sensitive columns
    sensitive_keywords = ["name", "iban", "account", "card", "address"]
    sensitive_columns = [
        c for c in df.columns
        if any(k in c.lower() for k in sensitive_keywords)
    ]

    # Simple quality score: inverse of missing + duplicates
    missing_avg = sum(missing_percentages.values()) / len(missing_percentages) if missing_percentages else 0
    quality_score = max(0.0, 100.0 - missing_avg - duplicate_rows)

    return DatasetProfile(
        dataset_id=dataset_id,
        rows=rows,
        columns=columns,
        data_types=data_types,
        missing_percentages=missing_percentages,
        unique_counts=unique_counts,
        duplicate_rows=duplicate_rows,
        amount_stats=amount_stats,
        date_ranges=date_ranges,
        currency_formats=currency_formats,
        sensitive_columns=sensitive_columns,
        quality_score=round(quality_score, 2),
    )
