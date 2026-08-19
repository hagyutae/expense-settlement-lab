"""R004 · 청구 기한 초과."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule
from core.domain.rules.registry import rule

LIMIT_DAYS = 30


@rule
class R004(RowRule):
    code = "R004"
    name = "청구 기한 초과"

    def check(self, expense):
        if expense.used_date is None or expense.claim_date is None:
            return None
        days = (expense.claim_date - expense.used_date).days
        if days <= LIMIT_DAYS:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message=f"사용일로부터 {LIMIT_DAYS}일이 지난 청구입니다 ({days}일)",
        )
