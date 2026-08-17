"""CSV 로더."""

import csv
import io

from core.domain.models import COLUMNS, Expense
from core.service.input.base import FileLoader


class CsvLoader(FileLoader):
    def supports(self, path):
        return str(path).lower().endswith(".csv")

    def parse(self, text):
        reader = csv.DictReader(io.StringIO(text))
        header = tuple(reader.fieldnames or ())
        if header != COLUMNS:
            raise ValueError(
                "헤더가 데이터 스키마와 다릅니다.\n"
                f"  기대: {', '.join(COLUMNS)}\n"
                f"  실제: {', '.join(header)}"
            )
        return [Expense(row) for row in reader]
