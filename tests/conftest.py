from pathlib import Path

import pytest

from container import build_service
from core.service.input.csv_loader import CsvLoader

FIXTURES = Path(__file__).parent / "rules" / "fixtures"


@pytest.fixture
def service():
    """등록된 규칙 전체. 골든 테스트가 쓴다."""
    return build_service()


@pytest.fixture
def settle():
    def _settle(rules, fixture_name):
        expenses = CsvLoader().load(FIXTURES / fixture_name)
        return build_service(rules).settle(expenses)

    return _settle
