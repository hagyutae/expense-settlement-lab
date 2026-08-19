"""네트워크 외부로 전송되는 도구 호출을 검사한다.

PreToolUse 로 걸린다. WebFetch 와 WebSearch, MCP 도구의 인자에 카드번호나
계좌번호, 주민등록번호가 있으면 호출을 거부한다.

이 도구들은 실행되는 순간 인자가 외부로 나간다. 나간 값은 회수하지 못하므로
결과를 가리는 PostToolUse 로는 늦다. 막을 수 있는 자리는 실행 전뿐이다.
"""

import json
import re
import sys

RRN = re.compile(r"(?<![\w-])\d{6}-[1-8]\d{6}(?![\w-])")
CARD_SPACED = re.compile(r"(?<![\w-])\d{4}[- ]\d{4}[- ]\d{4}[- ]\d{4}(?![\w-])")
CARD_PLAIN = re.compile(r"(?<![\w-])\d{16}(?![\w-])")
# 하이픈이 섞인 숫자 묶음. 숫자 개수로 계좌번호를 가려낸다.
# 날짜(2026-03-14)는 숫자가 여덟 개뿐이라 걸리지 않는다.
DIGIT_GROUP = re.compile(r"(?<![\w-])\d[\d-]*\d(?![\w-])")


def find_sensitive(text):
    """찾으면 (종류, 값), 없으면 None."""
    for name, pattern in (("주민등록번호", RRN),
                          ("카드번호", CARD_SPACED),
                          ("카드번호", CARD_PLAIN)):
        hit = pattern.search(text)
        if hit:
            return name, hit.group(0)

    for hit in DIGIT_GROUP.finditer(text):
        token = hit.group(0)
        digits = sum(char.isdigit() for char in token)
        if "-" in token and 10 <= digits <= 14:
            return "계좌번호", token
    return None


def run():
    data = json.load(sys.stdin)
    # 인자는 도구마다 필드가 다르다. 전체를 문자열로 펼쳐 한 번에 훑는다.
    payload = json.dumps(data.get("tool_input", {}), ensure_ascii=False)

    found = find_sensitive(payload)
    if not found:
        return

    kind, value = found
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"{kind}로 보이는 값이 외부 요청 인자에 포함돼 차단했습니다: {value}"
            ),
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    run()
