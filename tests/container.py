"""테스트가 쓰는 조립.

애플리케이션 컨테이너는 로더와 리포터까지 끼우지만 테스트에는 그것이 필요 없다.
테스트가 진입점 조립에 얹히면 CLI나 웹이 바뀔 때 테스트도 함께 흔들린다.
"""

from core.domain.rules.r001_required_fields import R001
from core.domain.rules.r002_amount_valid import R002
from core.domain.rules.r003_date_reversed import R003
from core.domain.rules.r004_claim_deadline import R004
from core.domain.rules.r005_receipt_no_missing import R005
from core.domain.rules.r006_meal_per_person import R006
from core.domain.rules.r007_lodging_limit import R007
from core.domain.rules.r008_transport_limit import R008
from core.domain.rules.r009_payment_method import R009
from core.domain.rules.r010_receipt_no_duplicated import R010
from core.domain.rules.r011_entertainment_attendees import R011
from core.domain.rules.r012_entertainment_per_person import R012
from core.domain.rules.r013_weekend_preapproval import R013
from core.domain.rules.r014_evidence_missing import R014
from core.domain.rules.r015_category_merchant import R015
from core.domain.rules.r016_personal_card_reason import R016
from core.domain.rules.r018_cash_limit import R018
from core.service.usecase.settlement import RuleBasedSettlementService


def all_rules():
    """구현한 규칙을 여기에 등록한다."""
    return [
        R001(), R002(), R003(), R004(), R005(),
        R006(), R007(), R008(), R009(), R010(),
        R011(), R012(), R013(), R014(), R015(),
        R016(), R018(),
    ]


def build_service(rules=None):
    """규칙을 주지 않으면 등록된 전체로 조립한다."""
    return RuleBasedSettlementService(all_rules() if rules is None else rules)
