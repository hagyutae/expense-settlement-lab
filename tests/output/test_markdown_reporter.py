"""서식 전체를 비교하지 않는다. 표가 만들어졌는지 구조만 본다."""

from core.domain.models import AggregationTable, Expense, Judgement, SettlementResult
from core.service.output.markdown_reporter import MarkdownReporter


def make_result():
    expense = Expense({"claim_id": "EXP-2026-0001", "employee_name": "김민준",
                       "used_date": "2026-07-01", "expense_type": "식비", "amount": "12000"})
    table = AggregationTable("부서별 정산 요약", ["부서", "청구"], [["영업1팀", 1]])
    return SettlementResult([Judgement(expense)], [table])


def test_has_judgement_table():
    out = MarkdownReporter().format(make_result())
    assert "| 청구ID |" in out
    assert "|---" in out
    assert "EXP-2026-0001" in out


def test_includes_aggregation_table():
    out = MarkdownReporter().format(make_result())
    assert "## 부서별 정산 요약" in out
    assert "| 부서 | 청구 |" in out
