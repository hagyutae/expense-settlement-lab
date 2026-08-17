"""규칙 베이스.

규칙 하나는 파일 하나입니다. 이 폴더에 `rXXX_설명.py` 로 만들고
`RowRule` 또는 `BatchRule` 중 맞는 쪽을 상속합니다.

클래스 이름과 메서드 이름은 바꾸지 마세요. 테스트와 이후 실습이 이 이름을 씁니다.
"""

from abc import ABC, abstractmethod


class Rule(ABC):
    """모든 규칙의 공통 베이스.

    `code` 와 `name` 은 `경비규정.md` 의 항목 제목에서 그대로 가져옵니다.
    `### R001 · 필수 항목 누락` 이면 code 는 `R001`, name 은 `필수 항목 누락` 입니다.
    위반을 만들 때 이 둘을 `Violation` 에 함께 넣습니다.
    """

    code: str
    name: str


class RowRule(Rule):
    """단건 규칙. 청구 한 건만 보고 판정합니다."""

    @abstractmethod
    def check(self, expense):
        """위반이면 `Violation`, 아니면 `None` 을 돌려줍니다."""
        ...


class BatchRule(Rule):
    """다건 규칙. 청구 전체를 함께 보고 판정합니다."""

    @abstractmethod
    def check_all(self, expenses):
        """위반이 걸린 항목의 위치와 `Violation` 을 돌려줍니다."""
        ...
