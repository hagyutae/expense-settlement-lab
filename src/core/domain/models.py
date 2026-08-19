"""도메인 모델.

속성은 docs/데이터-스키마.md 의 표를 보고 채웁니다.
클래스 이름은 바꾸지 마세요. 테스트와 이후 실습이 이 이름을 씁니다.
"""

from datetime import date

# 파일의 헤더 순서 그대로다. docs/데이터-스키마.md 의 컬럼 표를 따른다.
COLUMNS = (
    "claim_id", "employee_id", "employee_name", "department",
    "used_date", "claim_date", "expense_type", "amount",
    "payment_method", "merchant", "merchant_category", "evidence",
    "attendees", "receipt_no", "card_no", "bank_account", "resident_no", "note",
)
DATE_COLUMNS = ("used_date", "claim_date")
INT_COLUMNS = ("amount", "attendees")
TEXT_COLUMNS = tuple(c for c in COLUMNS if c not in DATE_COLUMNS + INT_COLUMNS)


def _to_date(value):
    """파싱에 실패하면 비운다. 값이 잘못되었는지 판단하는 것은 규칙의 몫이다."""
    try:
        return date.fromisoformat(str(value).strip())
    except (ValueError, TypeError):
        return None


def _to_int(value):
    text = str(value).strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


class Expense:
    """청구 한 건. 원본 문자열은 raw 에 그대로 두고 같은 이름의 속성으로 꺼내 쓴다."""

    def __init__(self, raw):
        self.raw = {c: str(raw.get(c, "")) for c in COLUMNS}
        for column in TEXT_COLUMNS:
            setattr(self, column, self.raw[column].strip())
        for column in DATE_COLUMNS:
            setattr(self, column, _to_date(self.raw[column]))
        for column in INT_COLUMNS:
            setattr(self, column, _to_int(self.raw[column]))

    def __repr__(self):
        return f"Expense({self.claim_id})"


class Violation:
    """규칙 하나가 잡아낸 위반."""

    def __init__(self, code, name, message):
        self.code = code
        self.name = name
        self.message = message

    def __repr__(self):
        return f"Violation({self.code})"


class Judgement:
    """청구 한 건의 판정. 위반 목록이 비면 통과다."""

    def __init__(self, expense, violations=()):
        self.expense = expense
        self.violations = list(violations)

    @property
    def is_passed(self):
        return not self.violations


class AggregationTable:
    """집계 하나가 만들어 낸 표."""

    def __init__(self, name, columns, rows):
        self.name = name
        self.columns = list(columns)
        self.rows = [list(row) for row in rows]

    def __repr__(self):
        return f"AggregationTable({self.name}, {len(self.rows)}행)"


class SettlementResult:
    """정산 한 번의 결과 전체."""

    def __init__(self, judgements, aggregations=()):
        self.judgements = list(judgements)
        self.aggregations = list(aggregations)
