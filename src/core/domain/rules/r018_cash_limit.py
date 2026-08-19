"""R018 · 현금 결제 한도."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule
from core.domain.rules.registry import rule

PAYMENT_METHOD = "현금"
LIMIT = 50_000


@rule
class R018(RowRule):
    code = "R018"
    name = "현금 결제 한도"

    def check(self, expense):
        if expense.payment_method != PAYMENT_METHOD or expense.amount is None:
            return None
        if expense.amount <= LIMIT:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message="현금 결제는 5만원까지만 인정됩니다",
        )
