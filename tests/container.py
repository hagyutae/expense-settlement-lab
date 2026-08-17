"""테스트가 쓰는 조립.

애플리케이션 컨테이너는 로더와 리포터까지 끼우지만 테스트에는 그것이 필요 없다.
테스트가 진입점 조립에 얹히면 CLI나 웹이 바뀔 때 테스트도 함께 흔들린다.
"""

from core.domain.rules.r001_required_fields import R001
from core.service.usecase.settlement import RuleBasedSettlementService


def all_rules():
    """구현한 규칙을 여기에 등록한다."""
    return [R001()]


def build_service(rules=None):
    """규칙을 주지 않으면 등록된 전체로 조립한다."""
    return RuleBasedSettlementService(all_rules() if rules is None else rules)
