from enum import Enum
from pydantic import BaseModel
from typing import Optional

class DatasetType(str, Enum):
    bank_transactions = "bank_transactions"
    general_ledger = "general_ledger"
    accounts_payable = "accounts_payable"
    accounts_receivable = "accounts_receivable"
    budget = "budget"

class RuleSeverity(str, Enum):
    info = "info"
    warning = "warning"
    error = "error"
    blocker = "blocker"

class Rule(BaseModel):
    name: str
    field: str
    condition: str
    severity: RuleSeverity
    action: str  # e.g. "require_user_review", "auto_normalise", "block_reconciliation"

class RuleResult(BaseModel):
    rule_name: str
    row_index: int
    field: str
    original_value: Optional[str]
    proposed_value: Optional[str]
    reason: str
    confidence: float

class Correction(BaseModel):
    row_index: int
    field: str
    original_value: Optional[str]
    proposed_value: Optional[str]
    reason: str
    confidence: float
    decision: Optional[str] = None  # "approve", "reject", "modify"

class AuditRecord(BaseModel):
    dataset_id: str
    dataset_version: str
    row_index: int
    field: str
    original_value: Optional[str]
    corrected_value: Optional[str]
    rule_applied: Optional[str]
    approved_by: Optional[str]
    approved_at: str
    override_reason: Optional[str]
