"""R021 · 교육훈련비 사전승인."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule
from core.domain.rules.registry import rule

EXPENSE_TYPE = "교육훈련비"
LIMIT = 200_000
PREFIX = "AP-"


@rule
class R021(RowRule):
    code = "R021"
    name = "교육훈련비 사전승인"

    def check(self, expense):
        if expense.expense_type != EXPENSE_TYPE or expense.amount is None:
            return None
        if expense.amount <= LIMIT:
            return None
        # 비고에 승인번호만 적기도 하고 설명과 함께 적기도 한다. 낱말 단위로 본다.
        if any(word.startswith(PREFIX) for word in expense.note.split()):
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message="20만원을 초과하는 교육훈련비는 사전승인 번호가 필요합니다",
        )
