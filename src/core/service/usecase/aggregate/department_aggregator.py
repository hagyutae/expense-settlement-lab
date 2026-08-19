"""부서별 정산 요약."""

from core.domain.models import AggregationTable
from core.service.usecase.aggregate.base import Aggregator
from core.service.usecase.aggregate.ops import count, ratio, select, total_amount


class DepartmentAggregator(Aggregator):
    name = "부서별 정산 요약"
    columns = ["부서", "청구", "통과", "반려", "반려율", "청구금액", "반려금액"]

    def aggregate(self, judgements):
        judgements = list(judgements)
        # 청구가 한 건도 없는 부서는 판정 목록에 나타나지 않으므로 저절로 빠진다.
        departments = sorted({j.expense.department for j in judgements})

        rows = []
        for department in departments:
            picked = select(judgements, department=department)
            rejected = select(picked, passed=False)
            rows.append([
                department,
                count(picked),
                count(select(picked, passed=True)),
                count(rejected),
                ratio(count(rejected), count(picked)),
                total_amount(picked),
                total_amount(rejected),
            ])

        rows.sort(key=lambda row: (-row[4], row[0]))
        return AggregationTable(self.name, self.columns, rows)
