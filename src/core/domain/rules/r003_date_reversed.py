"""R003 · 사용일자 역전."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule
from core.domain.rules.registry import rule


@rule
class R003(RowRule):
    code = "R003"
    name = "사용일자 역전"

    def check(self, expense):
        if expense.used_date is None or expense.claim_date is None:
            return None
        if expense.used_date <= expense.claim_date:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message="사용일자가 청구일자보다 뒤입니다",
        )
