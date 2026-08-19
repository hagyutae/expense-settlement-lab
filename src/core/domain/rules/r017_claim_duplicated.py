"""R017 · 중복 청구."""

from collections import defaultdict

from core.domain.models import Violation
from core.domain.rules.base import BatchRule
from core.domain.rules.registry import rule


@rule
class R017(BatchRule):
    code = "R017"
    name = "중복 청구"

    def check_all(self, expenses):
        positions = defaultdict(list)
        for i, expense in enumerate(expenses):
            key = (
                expense.employee_id,
                expense.used_date,
                expense.amount,
                expense.merchant,
            )
            # 판정에 쓰는 값이 하나라도 비면 같은 건인지 알 수 없다.
            if all(part not in (None, "") for part in key):
                positions[key].append(i)

        found = {}
        for indexes in positions.values():
            if len(indexes) < 2:
                continue
            for i in indexes:
                found[i] = Violation(
                    code=self.code,
                    name=self.name,
                    message=f"같은 내용으로 {len(indexes)}건이 중복 청구되었습니다",
                )
        return found
