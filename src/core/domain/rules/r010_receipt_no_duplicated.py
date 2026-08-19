"""R010 · 영수증번호 중복 사용."""

from collections import defaultdict

from core.domain.models import Violation
from core.domain.rules.base import BatchRule
from core.domain.rules.registry import rule


@rule
class R010(BatchRule):
    code = "R010"
    name = "영수증번호 중복 사용"

    def check_all(self, expenses):
        positions = defaultdict(list)
        for i, expense in enumerate(expenses):
            # 영수증번호가 비어 있는 건은 중복으로 보지 않는다.
            if expense.receipt_no:
                positions[expense.receipt_no].append(i)

        found = {}
        for indexes in positions.values():
            if len(indexes) < 2:
                continue
            for i in indexes:
                found[i] = Violation(
                    code=self.code,
                    name=self.name,
                    message=f"같은 영수증번호로 {len(indexes)}건이 청구되었습니다",
                )
        return found
