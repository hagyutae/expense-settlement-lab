"""골든 마스터 테스트.

`tests/golden/` 아래의 폴더를 모두 훑는다. 폴더 하나가 세트 하나이고,
`input.csv` 와 `expected.json` 한 쌍으로 이루어진다.

세트를 더할 때 이 파일을 고치지 않는다. 폴더를 놓으면 그대로 대상이 된다.
"""

import json
from pathlib import Path

import pytest

from core.service.input.csv_loader import CsvLoader

GOLDEN = Path(__file__).parent / "golden"
SETS = sorted(p for p in GOLDEN.iterdir() if p.is_dir())


@pytest.mark.parametrize("golden", SETS, ids=lambda p: p.name)
def test_golden(service, golden):
    expenses = CsvLoader().load(golden / "input.csv")
    result = service.settle(expenses)

    actual = [
        {
            "claim_id": j.expense.claim_id,
            "is_passed": j.is_passed,
            "violations": [v.code for v in j.violations],
        }
        for j in result.judgements
    ]
    expected = json.loads((golden / "expected.json").read_text(encoding="utf-8"))
    assert actual == expected
