"""R001 · 필수 항목 누락."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule
from core.domain.rules.registry import rule

REQUIRED = (
    "claim_id", "employee_id", "department", "used_date", "claim_date",
    "expense_type", "amount", "payment_method", "merchant",
)


@rule
class R001(RowRule):
    code = "R001"
    name = "필수 항목 누락"

    def check(self, expense):
        missing = [c for c in REQUIRED if not expense.raw[c].strip()]
        if not missing:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message=f"필수 항목이 비어 있습니다: {', '.join(missing)}",
        )
