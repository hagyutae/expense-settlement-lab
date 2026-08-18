"""R006 · 식비 1인 한도."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule

EXPENSE_TYPE = "식비"
LIMIT = 30_000


class R006(RowRule):
    code = "R006"
    name = "식비 1인 한도"

    def check(self, expense):
        if expense.expense_type != EXPENSE_TYPE or expense.amount is None:
            return None
        # 참석인원이 비어 있으면 1명으로 본다.
        attendees = expense.attendees if expense.attendees else 1
        per_person = expense.amount // attendees
        if per_person <= LIMIT:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message=f"식비 1인 한도 3만원을 초과했습니다 (1인 {per_person}원)",
        )
