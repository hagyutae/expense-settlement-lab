"""R020 · 1일 식비 중복."""

from collections import defaultdict

from core.domain.models import Violation
from core.domain.rules.base import BatchRule
from core.domain.rules.registry import rule

EXPENSE_TYPE = "식비"


@rule
class R020(BatchRule):
    code = "R020"
    name = "1일 식비 중복"

    def check_all(self, expenses):
        positions = defaultdict(list)
        for i, expense in enumerate(expenses):
            if expense.expense_type != EXPENSE_TYPE:
                continue
            if not expense.employee_id or expense.used_date is None:
                continue
            positions[(expense.employee_id, expense.used_date)].append(i)

        found = {}
        for indexes in positions.values():
            if len(indexes) < 2:
                continue
            for i in indexes:
                found[i] = Violation(
                    code=self.code,
                    name=self.name,
                    message=f"같은 날 식비가 {len(indexes)}건 청구되었습니다",
                )
        return found
