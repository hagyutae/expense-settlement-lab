"""R019 · 부서 월 한도 초과."""

from collections import defaultdict

from core.domain.models import Violation
from core.domain.rules.base import BatchRule
from core.domain.rules.registry import rule

MONTHLY_LIMIT = {
    "영업1팀": 5_000_000,
    "개발2팀": 3_000_000,
    "마케팅팀": 4_000_000,
    "경영지원팀": 2_000_000,
    "연구소": 3_000_000,
}


@rule
class R019(BatchRule):
    code = "R019"
    name = "부서 월 한도 초과"

    def check_all(self, expenses):
        groups = defaultdict(list)
        for i, expense in enumerate(expenses):
            if expense.used_date is None or expense.amount is None:
                continue
            if expense.department not in MONTHLY_LIMIT:
                continue
            key = (expense.department, expense.used_date.strftime("%Y-%m"))
            groups[key].append((expense.used_date, i, expense.amount))

        found = {}
        for (department, month), rows in groups.items():
            limit = MONTHLY_LIMIT[department]
            running = 0
            exceeded = False
            # 사용일자 오름차순으로 누적한다. 같은 날은 파일 순서를 따른다.
            for _, i, amount in sorted(rows):
                running += amount
                if running > limit:
                    exceeded = True
                if exceeded:
                    found[i] = Violation(
                        code=self.code,
                        name=self.name,
                        message=(
                            f"{department} {month} 한도를 초과했습니다 "
                            f"(누적 {running:,}원)"
                        ),
                    )
        return found
