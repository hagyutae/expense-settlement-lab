"""조립.

추상과 구현이 만나는 유일한 지점입니다.
**규칙은 명시적으로 나열해 등록합니다. 모듈을 스캔해 자동으로 모으지 않습니다.**

함수 이름은 바꾸지 마세요. CLI가 이 이름을 씁니다.
"""


def build_loader(fmt):
    """형식에 맞는 `Loader`.

    확장자를 보고 형식을 정하는 일은 진입점이 맡습니다. 조립은 형식 이름만 받습니다.
    """
    ...


def build_service():
    """규칙이 주입된 `SettlementService`."""
    ...


def build_reporter(fmt):
    """형식에 맞는 `Reporter`."""
    ...
