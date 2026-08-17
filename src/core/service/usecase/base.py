"""처리 추상.

클래스 이름과 메서드 이름은 바꾸지 마세요. 테스트와 이후 실습이 이 이름을 씁니다.
"""

from abc import ABC, abstractmethod


class SettlementService(ABC):
    """청구 목록을 판정합니다. 파일 경로를 받지 않습니다."""

    @abstractmethod
    def settle(self, expenses):
        """`SettlementResult`. 입력 순서를 유지합니다."""
        ...
