from typing import List, Dict
import json
import pandas as pd
from pydantic import BaseModel
from models import Rule, RuleResult, RuleSeverity

RULE_TEMPLATES_PATH = "storage/rule_templates"

class RuleTemplate(BaseModel):
    name: str
    description: str
    rules: List[Rule]

    def save(self):
        path = f"{RULE_TEMPLATES_PATH}/{self.name}.json"
        with open(path, "w") as f:
            f.write(self.json(indent=2))

    @classmethod
    def load(cls, name: str) -> "RuleTemplate":
        path = f"{RULE_TEMPLATES_PATH}/{name}.json"
        with open(path) as f:
            data = json.load(f)
        return cls(**data)

def apply_rules(df: pd.DataFrame, template: RuleTemplate) -> List[RuleResult]:
    results: List[RuleResult] = []

    for rule in template.rules:
        if rule.condition == "value_is_missing":
            if rule.field in df.columns:
                missing_indices = df[df[rule.field].isna()].index
                for idx in missing_indices:
                    results.append(
                        RuleResult(
                            rule_name=rule.name,
                            row_index=int(idx),
                            field=rule.field,
                            original_value=None,
                            proposed_value=None,
                            reason=f"{rule.field} is required but missing",
                            confidence=1.0,
                        )
                    )

        if rule.name == "standardise_transaction_date":
            if rule.field in df.columns:
                parsed = pd.to_datetime(df[rule.field], errors="coerce", dayfirst=True)
                for idx, (orig, new) in enumerate(zip(df[rule.field], parsed)):
                    if pd.isna(new):
                        continue
                    if str(orig) != new.isoformat():
                        results.append(
                            RuleResult(
                                rule_name=rule.name,
                                row_index=int(idx),
                                field=rule.field,
                                original_value=str(orig),
                                proposed_value=new.isoformat(),
                                reason="Date normalised to ISO format",
                                confidence=0.98,
                            )
                        )

        # Additional finance-specific rules can be added here:
        # - debit/credit reconciliation
        # - mixed currencies
        # - duplicate transactions, etc.

    return results
