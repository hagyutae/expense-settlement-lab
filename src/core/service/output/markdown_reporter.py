"""Markdown 표 출력."""

from collections import Counter

from core.service.output.base import Reporter

HEADERS = ("청구ID", "성명", "사용일자", "계정과목", "금액", "판정", "위반")


def _table(columns, rows):
    lines = ["| " + " | ".join(str(c) for c in columns) + " |"]
    lines.append("|" + "|".join(["---"] * len(columns)) + "|")
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return lines


class MarkdownReporter(Reporter):
    def format(self, result):
        rows = [
            (
                j.expense.claim_id,
                j.expense.employee_name,
                j.expense.raw["used_date"],
                j.expense.expense_type,
                f"{j.expense.amount:,}" if j.expense.amount is not None else "",
                "통과" if j.is_passed else "반려",
                " ".join(v.code for v in j.violations),
            )
            for j in result.judgements
        ]

        lines = ["## 판정", ""]
        lines += _table(HEADERS, rows)

        rejected = [j for j in result.judgements if not j.is_passed]
        counts = Counter(v.code for j in rejected for v in j.violations)
        names = {v.code: v.name for j in rejected for v in j.violations}

        lines += ["", "## 요약", ""]
        lines.append(
            f"- 전체 {len(result.judgements)}건 · 통과 "
            f"{len(result.judgements) - len(rejected)} · 반려 {len(rejected)}"
        )
        for code in sorted(counts):
            lines.append(f"- {code} {names[code]}: {counts[code]}건")

        # 어떤 집계가 들어 있는지 알지 못한다. 순서대로 표로 그린다.
        for table in result.aggregations:
            lines += ["", f"## {table.name}", ""]
            lines += _table(
                table.columns,
                [[f"{c:,}" if isinstance(c, int) else c for c in row] for row in table.rows],
            )

        return "\n".join(lines)
