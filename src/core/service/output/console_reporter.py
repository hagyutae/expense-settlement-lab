"""터미널 출력."""

from collections import Counter

from core.service.output.base import Reporter

HEADERS = ("청구ID", "성명", "사용일자", "계정과목", "금액", "판정", "위반")


def _width(text):
    """한글은 두 칸을 차지한다. 고정폭 정렬을 맞추려면 그만큼 세어야 한다."""
    return sum(2 if ord(c) > 0x2E7F else 1 for c in str(text))


def _pad(text, width, align="left"):
    space = " " * max(0, width - _width(text))
    return space + str(text) if align == "right" else str(text) + space


class ConsoleReporter(Reporter):
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

        widths = [
            max(_width(HEADERS[i]), *(_width(r[i]) for r in rows)) if rows else _width(HEADERS[i])
            for i in range(len(HEADERS))
        ]
        right = {4}

        lines = ["  ".join(_pad(h, widths[i]) for i, h in enumerate(HEADERS)).rstrip()]
        for row in rows:
            lines.append(
                "  ".join(
                    _pad(cell, widths[i], "right" if i in right else "left")
                    for i, cell in enumerate(row)
                ).rstrip()
            )

        rejected = [j for j in result.judgements if not j.is_passed]
        lines.append("")
        lines.append(
            f"전체 {len(result.judgements)}건 · 통과 {len(result.judgements) - len(rejected)}"
            f" · 반려 {len(rejected)}"
        )

        counts = Counter(v.code for j in rejected for v in j.violations)
        names = {v.code: v.name for j in rejected for v in j.violations}
        for code in sorted(counts):
            lines.append(f"{code} {names[code]}  {counts[code]}건")

        return "\n".join(lines)
