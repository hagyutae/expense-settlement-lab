"""규칙이 컨테이너 두 곳에 등록되지 않았으면 커밋을 막는다.

한 곳만 등록하면 그 규칙의 테스트는 통과하므로 사람 눈에 띄지 않는다.
"""

import json
import re
import sys
from pathlib import Path

CONTAINERS = (
    ("src/application/container.py", "build_service"),
    ("tests/container.py", "all_rules"),
)

data = json.load(sys.stdin)
if "git commit" not in data.get("tool_input", {}).get("command", ""):
    sys.exit(0)

root = Path.cwd()
codes = sorted(
    path.name[:4].upper()
    for path in (root / "src/core/domain/rules").glob("r[0-9][0-9][0-9]_*.py")
)

missing = []
for relative, function in CONTAINERS:
    body = (root / relative).read_text(encoding="utf-8").split(f"def {function}")[-1]
    missing += [
        f"{code} 가 {relative} 의 {function}() 에 등록되지 않았습니다"
        for code in codes
        if not re.search(rf"\b{code}\b", body)
    ]

if missing:
    print("\n".join(missing), file=sys.stderr)
    sys.exit(2)
