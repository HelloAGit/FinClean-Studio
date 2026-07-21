from typing import List
import pandas as pd
from pydantic import BaseModel
from models import RuleResult, Correction, AuditRecord
from storage.files import load_dataset, save_cleaned_dataset
from datetime import datetime
import uuid

class CorrectionDecisionRequest(BaseModel):
    row_index: int
    field: str
    decision: str  # "approve", "reject", "modify"
    modified_value: str | None = None
    user: str
    reason: str | None = None

def generate_corrections(df: pd.DataFrame, rule_results: List[RuleResult]) -> List[Correction]:
    corrections: List[Correction] = []
    for r in rule_results:
        corrections.append(
            Correction(
                row_index=r.row_index,
                field=r.field,
                original_value=r.original_value,
                proposed_value=r.proposed_value,
                reason=r.reason,
                confidence=r.confidence,
            )
        )
    return corrections

def apply_decisions(dataset_id: str, decisions: List[CorrectionDecisionRequest]):
    df = load_dataset(dataset_id)
    audit_log: List[AuditRecord] = []
    dataset_version = str(uuid.uuid4())

    for d in decisions:
        original_value = df.at[d.row_index, d.field]
        corrected_value = original_value

        if d.decision == "approve":
            # Use proposed value (already computed by rules engine)
            corrected_value = d.modified_value if d.modified_value is not None else df.at[d.row_index, d.field]
        elif d.decision == "modify":
            corrected_value = d.modified_value
        elif d.decision == "reject":
            corrected_value = original_value

        df.at[d.row_index, d.field] = corrected_value

        audit_log.append(
            AuditRecord(
                dataset_id=dataset_id,
                dataset_version=dataset_version,
                row_index=d.row_index,
                field=d.field,
                original_value=str(original_value),
                corrected_value=str(corrected_value),
                rule_applied=None,  # could be linked to RuleResult
                approved_by=d.user,
                approved_at=datetime.utcnow().isoformat(),
                override_reason=d.reason,
            )
        )

    cleaned_path = save_cleaned_dataset(dataset_id, df, dataset_version)
    return df, audit_log
