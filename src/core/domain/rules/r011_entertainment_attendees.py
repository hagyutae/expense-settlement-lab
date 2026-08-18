"""R011 · 접대비 참석인원 누락."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule

EXPENSE_TYPE = "접대비"


class R011(RowRule):
    code = "R011"
    name = "접대비 참석인원 누락"

    def check(self, expense):
        if expense.expense_type != EXPENSE_TYPE:
            return None
        if expense.attendees is not None and expense.attendees > 0:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message="접대비는 참석인원을 입력해야 합니다",
        )
