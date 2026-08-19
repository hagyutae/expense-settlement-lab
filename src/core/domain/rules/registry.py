"""규칙 레지스트리.

규칙 클래스에 `@rule` 을 붙이면 임포트되는 순간 목록에 들어갑니다.
`load_rules()` 가 이 폴더의 규칙 모듈을 모두 임포트하고 등록된 규칙을 돌려줍니다.

조립하는 쪽은 규칙 이름을 나열하지 않습니다. 파일을 추가하면 그것으로 끝입니다.
"""

import importlib
import pkgutil
import re

_REGISTERED = {}

MODULE_PATTERN = re.compile(r"r\d{3}_")


def rule(cls):
    """규칙 클래스를 레지스트리에 넣습니다."""
    _REGISTERED[cls.code] = cls
    return cls


def load_rules():
    """규칙 인스턴스 전체. 규칙 코드 순으로 돌려줍니다."""
    package = importlib.import_module(__package__)
    for info in pkgutil.iter_modules(package.__path__):
        if MODULE_PATTERN.match(info.name):
            importlib.import_module(f"{package.__name__}.{info.name}")
    return [_REGISTERED[code]() for code in sorted(_REGISTERED)]
