"""규칙 기반 정산."""

from core.service.usecase.base import SettlementService


class RuleBasedSettlementService(SettlementService):
    """규칙 목록을 생성자로 주입받습니다."""

    def __init__(self, rules):
        ...

    def settle(self, expenses):
        ...
