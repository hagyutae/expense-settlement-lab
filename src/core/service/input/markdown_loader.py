"""Markdown 표 로더."""

from core.domain.models import COLUMNS, Expense
from core.service.input.base import FileLoader

SEPARATOR = set("-: |")


def _cells(line):
    """`| a | b |` 한 줄을 셀 목록으로 나눕니다."""
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


class MarkdownLoader(FileLoader):
    def supports(self, path):
        return str(path).lower().endswith(".md")

    def parse(self, text):
        lines = [line for line in text.splitlines() if line.strip().startswith("|")]
        if not lines:
            raise ValueError("Markdown 표를 찾지 못했습니다.")

        header = tuple(_cells(lines[0]))
        if header != COLUMNS:
            raise ValueError(
                "헤더가 데이터 스키마와 다릅니다.\n"
                f"  기대: {', '.join(COLUMNS)}\n"
                f"  실제: {', '.join(header)}"
            )

        rows = []
        for line in lines[1:]:
            # 헤더 바로 아래의 구분 행은 하이픈과 콜론만으로 이루어져 있다.
            if set(line.strip()) <= SEPARATOR:
                continue
            rows.append(Expense(dict(zip(COLUMNS, _cells(line)))))
        return rows
