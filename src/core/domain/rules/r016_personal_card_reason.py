"""R016 · 개인카드 사용 사유 누락."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule

PAYMENT_METHOD = "개인카드"


class R016(RowRule):
    code = "R016"
    name = "개인카드 사용 사유 누락"

    def check(self, expense):
        if expense.payment_method != PAYMENT_METHOD or expense.note:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message="개인카드 사용 시 비고에 사유를 입력해야 합니다",
        )
