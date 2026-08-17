"""출력 추상.

클래스 이름과 메서드 이름은 바꾸지 마세요. 테스트와 이후 실습이 이 이름을 씁니다.
"""

from abc import ABC, abstractmethod


class Reporter(ABC):
    """결과를 사람이 읽을 문자열로 바꿉니다.

    문자열을 돌려주기만 합니다. 화면에 쓰거나 파일로 저장하지 않습니다.
    요약에 쓰는 규칙 이름은 `Violation` 에서 읽습니다.
    """

    @abstractmethod
    def format(self, result):
        ...
