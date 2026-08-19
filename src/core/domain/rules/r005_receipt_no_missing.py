"""R005 · 영수증번호 누락."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule
from core.domain.rules.registry import rule

THRESHOLD = 30_000


@rule
class R005(RowRule):
    code = "R005"
    name = "영수증번호 누락"

    def check(self, expense):
        if expense.amount is None or expense.amount <= THRESHOLD:
            return None
        if expense.receipt_no:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message="3만원을 초과하는 청구에는 영수증번호가 필요합니다",
        )
