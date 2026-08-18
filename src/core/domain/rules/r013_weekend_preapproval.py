"""R013 · 주말 사용 사전승인."""

from core.domain.models import Violation
from core.domain.rules.base import RowRule

PREAPPROVAL_PREFIX = "A-"


class R013(RowRule):
    code = "R013"
    name = "주말 사용 사전승인"

    def check(self, expense):
        if expense.used_date is None or expense.used_date.weekday() < 5:
            return None
        if any(token.startswith(PREAPPROVAL_PREFIX) for token in expense.note.split()):
            return None
        return Violation(
            code=self.code,
            name=self.name,
            message="주말 사용 건은 사전승인 번호가 필요합니다",
        )
