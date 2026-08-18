"""R007 · 숙박비 한도."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule

EXPENSE_TYPE = "숙박비"
LIMIT = 200_000


class R007(RowRule):
    code = "R007"
    name = "숙박비 한도"

    def check(self, expense):
        if expense.expense_type != EXPENSE_TYPE or expense.amount is None:
            return None
        if expense.amount <= LIMIT:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message="숙박비 건당 한도 20만원을 초과했습니다",
        )
