"""R009 · 결제수단 값 오류."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule
from core.domain.rules.registry import rule

ALLOWED = ("법인카드", "개인카드", "현금")


@rule
class R009(RowRule):
    code = "R009"
    name = "결제수단 값 오류"

    def check(self, expense):
        if expense.payment_method in ALLOWED:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message=f"결제수단 값이 올바르지 않습니다: {expense.payment_method}",
        )
