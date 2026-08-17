"""조립.

추상과 구현이 만나는 유일한 지점입니다.
**규칙은 명시적으로 나열해 등록합니다. 모듈을 스캔해 자동으로 모으지 않습니다.**

함수 이름은 바꾸지 마세요. CLI가 이 이름을 씁니다.
"""

from core.domain.rules.r001_required_fields import R001
from core.service.input.csv_loader import CsvLoader
from core.service.output.console_reporter import ConsoleReporter
from core.service.usecase.settlement import RuleBasedSettlementService

LOADERS = {"csv": CsvLoader}
REPORTERS = {"console": ConsoleReporter}


def build_loader(fmt):
    """형식에 맞는 `Loader`.

    확장자를 보고 형식을 정하는 일은 진입점이 맡습니다. 조립은 형식 이름만 받습니다.
    """
    if fmt not in LOADERS:
        raise ValueError(
            f"지원하지 않는 입력 형식입니다: {fmt} (가능: {', '.join(sorted(LOADERS))})"
        )
    return LOADERS[fmt]()


def build_service():
    """규칙이 주입된 `SettlementService`."""
    return RuleBasedSettlementService([R001()])


def build_reporter(fmt):
    """형식에 맞는 `Reporter`."""
    if fmt not in REPORTERS:
        raise ValueError(
            f"지원하지 않는 출력 형식입니다: {fmt} (가능: {', '.join(sorted(REPORTERS))})"
        )
    return REPORTERS[fmt]()
