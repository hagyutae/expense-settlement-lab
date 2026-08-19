"""규칙 기반 정산."""

from core.domain.models import Judgement, SettlementResult
from core.domain.rules.base import BatchRule, RowRule
from core.service.usecase.base import SettlementService


class RuleBasedSettlementService(SettlementService):
    """규칙 목록과 집계 목록을 생성자로 주입받습니다."""

    def __init__(self, rules, aggregators=()):
        self.rules = list(rules)
        self.aggregators = list(aggregators)

    def settle(self, expenses):
        expenses = list(expenses)
        found = {i: [] for i in range(len(expenses))}

        for rule in self.rules:
            if isinstance(rule, RowRule):
                for i, expense in enumerate(expenses):
                    violation = rule.check(expense)
                    if violation is not None:
                        found[i].append(violation)
            elif isinstance(rule, BatchRule):
                for i, violation in rule.check_all(expenses).items():
                    found[i].append(violation)

        judgements = [
            Judgement(expense, sorted(found[i], key=lambda v: v.code))
            for i, expense in enumerate(expenses)
        ]
        # 집계는 판정이 끝난 뒤에 돈다. 판정을 바꾸지 않는다.
        return SettlementResult(
            judgements,
            [aggregator.aggregate(judgements) for aggregator in self.aggregators],
        )
