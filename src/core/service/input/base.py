"""입력 추상.

클래스 이름과 메서드 이름은 바꾸지 마세요. 테스트와 이후 실습이 이 이름을 씁니다.
"""

from abc import ABC, abstractmethod


class Loader(ABC):
    """청구 목록을 만들어 내는 것. 입력원이 무엇인지 규정하지 않습니다."""

    @abstractmethod
    def load(self, source):
        """`Expense` 목록. 원본 순서를 유지합니다."""
        ...


class FileLoader(Loader):
    """파일에서 읽는 로더. 파일을 여는 일과 인코딩을 여기서 처리합니다.

    구체 로더는 `supports` 와 `parse` 둘만 구현합니다.
    """

    def load(self, path):
        """파일을 읽어 `parse` 에 넘깁니다."""
        ...

    @abstractmethod
    def supports(self, path):
        """이 로더가 처리할 수 있는 파일인지 돌려줍니다."""
        ...

    @abstractmethod
    def parse(self, text):
        """읽어 들인 텍스트를 `Expense` 목록으로 바꿉니다."""
        ...
