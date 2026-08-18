"""R008 · 교통비 한도."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule

EXPENSE_TYPE = "교통비"
LIMIT = 100_000


class R008(RowRule):
    code = "R008"
    name = "교통비 한도"

    def check(self, expense):
        if expense.expense_type != EXPENSE_TYPE or expense.amount is None:
            return None
        if expense.amount <= LIMIT:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message="교통비 건당 한도 10만원을 초과했습니다",
        )
