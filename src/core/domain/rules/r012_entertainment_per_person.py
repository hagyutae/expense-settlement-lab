"""R012 · 접대비 1인 한도."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule

EXPENSE_TYPE = "접대비"
LIMIT = 50_000


class R012(RowRule):
    code = "R012"
    name = "접대비 1인 한도"

    def check(self, expense):
        if expense.expense_type != EXPENSE_TYPE or expense.amount is None:
            return None
        # 참석인원이 없으면 R011이 잡는다. 여기서는 1인당 금액을 낼 수 없어 넘긴다.
        if not expense.attendees or expense.attendees <= 0:
            return None
        per_person = expense.amount // expense.attendees
        if per_person <= LIMIT:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message=f"접대비 1인 한도 5만원을 초과했습니다 (1인 {per_person}원)",
        )
