"""R014 · 적격증빙 누락."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule
from core.domain.rules.registry import rule

LIMIT = 50_000


@rule
class R014(RowRule):
    code = "R014"
    name = "적격증빙 누락"

    def check(self, expense):
        if expense.amount is None or expense.amount <= LIMIT:
            return None
        if expense.evidence != "N":
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message="5만원을 초과하는 청구에는 적격증빙이 필요합니다",
        )
