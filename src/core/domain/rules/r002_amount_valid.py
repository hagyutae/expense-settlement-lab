"""R002 · 금액 유효성."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule


class R002(RowRule):
    code = "R002"
    name = "금액 유효성"

    def check(self, expense):
        if expense.amount is not None and expense.amount > 0:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message=f"금액이 유효하지 않습니다: {expense.raw['amount'].strip()}",
        )
