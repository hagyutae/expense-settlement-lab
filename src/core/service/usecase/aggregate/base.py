"""집계 추상.

집계 하나는 파일 하나입니다. 이 폴더에 만들고 `Aggregator` 를 상속합니다.

클래스 이름과 메서드 이름은 바꾸지 마세요. 테스트와 출력 계층이 이 이름을 씁니다.
"""

from abc import ABC, abstractmethod


class Aggregator(ABC):
    """판정 목록을 기준에 따라 묶어 표 하나를 만듭니다.

    결과가 어디에 담기는지 알지 못합니다. 표를 돌려주기만 합니다.
    """

    @property
    @abstractmethod
    def name(self):
        """표 제목."""
        ...

    @property
    @abstractmethod
    def columns(self):
        """열 이름 목록."""
        ...

    @abstractmethod
    def aggregate(self, judgements):
        """`AggregationTable`."""
        ...
