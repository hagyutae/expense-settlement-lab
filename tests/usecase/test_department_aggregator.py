"""판정 목록을 손으로 만들어 넣고 표를 대조한다."""

from core.domain.models import Expense, Judgement, Violation
from core.service.usecase.aggregate.department_aggregator import DepartmentAggregator

REJECT = Violation("R002", "금액 유효성", "금액이 올바르지 않습니다")


def judgement(department, amount, passed=True):
    expense = Expense({"department": department, "amount": amount})
    return Judgement(expense, () if passed else (REJECT,))


def test_columns_and_rows():
    table = DepartmentAggregator().aggregate([
        judgement("영업1팀", 100000),
        judgement("영업1팀", 200000, passed=False),
        judgement("영업1팀", 300000),
        judgement("개발2팀", 400000),
    ])

    assert table.name == "부서별 정산 요약"
    assert table.columns == ["부서", "청구", "통과", "반려", "반려율", "청구금액", "반려금액"]
    # 반려율 내림차순
    assert table.rows == [
        ["영업1팀", 3, 2, 1, 33.3, 600000, 200000],
        ["개발2팀", 1, 1, 0, 0.0, 400000, 0],
    ]


def test_empty_amount_counts_as_zero():
    table = DepartmentAggregator().aggregate([
        judgement("연구소", ""),
        judgement("연구소", 50000),
    ])
    assert table.rows == [["연구소", 2, 2, 0, 0.0, 50000, 0]]
