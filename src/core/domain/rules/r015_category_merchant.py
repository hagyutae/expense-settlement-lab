"""R015 · 계정과목·업종 불일치."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule
from core.domain.rules.registry import rule

ALLOWED = {
    "식비": ("음식점",),
    "접대비": ("음식점", "주점"),
    "교통비": ("교통",),
    "숙박비": ("숙박",),
    "도서구입비": ("서점",),
    "소모품비": ("문구", "기타"),
    "통신비": ("통신",),
    "교육훈련비": ("기타",),
}


@rule
class R015(RowRule):
    code = "R015"
    name = "계정과목·업종 불일치"

    def check(self, expense):
        allowed = ALLOWED.get(expense.expense_type)
        if allowed is None or expense.merchant_category in allowed:
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message=(
                f"계정과목 {expense.expense_type}에 맞지 않는 업종입니다: "
                f"{expense.merchant_category}"
            ),
        )
