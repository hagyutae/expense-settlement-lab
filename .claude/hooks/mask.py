"""도구가 돌려준 결과에서 민감정보를 가린다.

PostToolUse 로 걸린다. 도구가 이미 실행된 뒤, 그 결과가 모델에 전달되기 전에
카드번호와 계좌번호, 주민등록번호를 가려 updatedToolOutput 으로 돌려준다.

Bash 는 stdout 과 stderr 를, Read 는 file.content 를 고친다. 돌려주는 값은
도구의 출력 모양을 그대로 지켜야 한다. 어긋나면 오류가 기록되고 원본이 그대로
모델에 전달된다. 그래서 받은 응답을 통째로 갈아치우지 않고 값만 고쳐 돌려준다.

네트워크 외부로 전송되는 값은 여기서 막지 못한다. 도구가 이미 보낸 뒤이기
때문이다. 그쪽은 guard.py 가 PreToolUse 에서 맡는다.
"""

import json
import re
import sys


def mask_tail(token, keep):
    """숫자와 구분자가 섞인 토큰에서 끝 `keep` 자리만 남기고 숫자를 * 로 바꾼다."""
    total = sum(char.isdigit() for char in token)
    seen = 0
    out = []
    for char in token:
        if char.isdigit():
            seen += 1
            out.append(char if seen > total - keep else "*")
        else:
            out.append(char)
    return "".join(out)


def mask_text(text):
    # 1. 주민등록번호(6-7): 생년월일 여섯 자리만 남기고 뒤 일곱 자리를 가린다.
    text = re.sub(
        r"(?<![\w-])(\d{6})-[1-8]\d{6}(?![\w-])",
        lambda m: m.group(1) + "-" + "*" * 7,
        text,
    )
    # 2. 카드번호(4-4-4-4, 하이픈 또는 공백): 끝 네 자리만 남긴다.
    text = re.sub(
        r"(?<![\w-])\d{4}[- ]\d{4}[- ]\d{4}[- ]\d{4}(?![\w-])",
        lambda m: mask_tail(m.group(0), 4),
        text,
    )
    # 3. 카드번호(붙여 쓴 16자리): 끝 네 자리만 남긴다.
    text = re.sub(
        r"(?<![\w-])\d{16}(?![\w-])",
        lambda m: mask_tail(m.group(0), 4),
        text,
    )
    # 4. 계좌번호: 하이픈이 섞인 숫자 묶음 중 숫자가 10~14자리인 것. 끝 세 자리만 남긴다.
    #    날짜(2026-03-14, 숫자 8자리)와 영수증 ID(R-... 앞에 문자)는 걸리지 않는다.
    def mask_account(m):
        token = m.group(0)
        digits = sum(char.isdigit() for char in token)
        if "-" in token and 10 <= digits <= 14:
            return mask_tail(token, 3)
        return token

    return re.sub(r"(?<![\w-])\d[\d-]*\d(?![\w-])", mask_account, text)


def run():
    data = json.load(sys.stdin)
    response = data.get("tool_response")
    if not isinstance(response, dict):
        return

    changed = False
    # Bash: stdout 과 stderr 를 그대로 두고 값만 고친다.
    if "stdout" in response:
        response["stdout"] = mask_text(response.get("stdout") or "")
        response["stderr"] = mask_text(response.get("stderr") or "")
        changed = True
    # Read: {"type": "text", "file": {..., "content": ...}} 안의 content 만 고친다.
    file_part = response.get("file")
    if isinstance(file_part, dict) and "content" in file_part:
        file_part["content"] = mask_text(file_part["content"])
        changed = True

    if changed:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "updatedToolOutput": response,
            }
        }, ensure_ascii=False))


if __name__ == "__main__":
    run()
