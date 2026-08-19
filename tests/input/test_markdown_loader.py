"""같은 내용을 두 형식으로 두고 판정이 같은지 본다."""

from pathlib import Path

from container import build_service
from core.service.input.csv_loader import CsvLoader
from core.service.input.markdown_loader import MarkdownLoader

SAMPLES = Path(__file__).resolve().parents[2] / "samples"


def codes(expenses):
    result = build_service().settle(expenses)
    return [(j.expense.claim_id, [v.code for v in j.violations]) for j in result.judgements]


def test_markdown_matches_csv():
    csv_rows = CsvLoader().load(SAMPLES / "영업1팀.csv")
    md_rows = MarkdownLoader().load(SAMPLES / "영업1팀.md")

    assert [e.claim_id for e in md_rows] == [e.claim_id for e in csv_rows]
    assert codes(md_rows) == codes(csv_rows)
