"""도메인 객체를 응답 모델로 옮긴다.

`core` 는 응답 형식을 알지 못합니다. 그 간극을 여기서 메웁니다.
요약은 판정 목록에서 세어 만듭니다. `core` 에 요약 계산을 넣지 않습니다.
"""

from application.web.schema import (
    AggregationTable,
    Judgement,
    SettlementResponse,
    Summary,
    Violation,
)


def to_summary(judgements):
    """판정 목록에서 건수를 센다."""
    passed = sum(1 for j in judgements if j.is_passed)
    return Summary(
        total=len(judgements), passed=passed, rejected=len(judgements) - passed
    )


def to_judgement(j):
    return Judgement(
        claim_id=j.expense.claim_id,
        employee_name=j.expense.employee_name,
        department=j.expense.department,
        used_date=j.expense.raw["used_date"],
        expense_type=j.expense.expense_type,
        amount=j.expense.amount,
        is_passed=j.is_passed,
        violations=[
            Violation(code=v.code, name=v.name, message=v.message) for v in j.violations
        ],
    )


def to_response(result):
    return SettlementResponse(
        summary=to_summary(result.judgements),
        judgements=[to_judgement(j) for j in result.judgements],
        aggregations=[
            AggregationTable(name=t.name, columns=t.columns, rows=t.rows)
            for t in result.aggregations
        ],
    )
