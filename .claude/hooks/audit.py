"""모든 도구 호출을 .claude/audit.jsonl 에 한 줄씩 남긴다.

PostToolUse 입력을 읽어 시각 · 도구 이름 · 인자 요약을 JSON 한 줄로 적는다.
카드 · 계좌 · 주민번호는 mask.py 의 규칙으로 가린 뒤 기록하므로 원본이
로그에 남지 않는다. 파일 경로와 명령까지만 남기는 저장소 규약을 따른다.

훅은 감사 기록이 목적이므로 무슨 일이 있어도 도구 실행을 막지 않는다.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mask import mask_text  # noqa: E402

LOG_PATH = Path(".claude/audit.jsonl")

# 요약이 길어지면 이만큼에서 자른다. 로그 한 줄이 지나치게 커지지 않게 한다.
MAX_SUMMARY = 300


def summarize(tool, tool_input):
    """도구별로 인자에서 핵심만 뽑아 한 줄 문자열로 만든다."""
    if not isinstance(tool_input, dict):
        return str(tool_input)

    if tool == "Bash":
        summary = tool_input.get("command", "")
    elif tool in ("Read", "Edit", "Write", "NotebookEdit"):
        summary = tool_input.get("file_path", "") or tool_input.get("notebook_path", "")
    else:
        # 모르는 도구는 키만 나열한다. 값에는 민감정보가 있을 수 있어 담지 않는다.
        summary = ", ".join(sorted(tool_input))

    summary = " ".join(summary.split())
    if len(summary) > MAX_SUMMARY:
        summary = summary[:MAX_SUMMARY] + "…"
    return summary


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return

    tool = data.get("tool_name", "")
    entry = {
        "time": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "tool": tool,
        "args": mask_text(summarize(tool, data.get("tool_input", {}))),
    }

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as log:
        log.write(json.dumps(entry, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # 감사 훅은 도구 실행을 막지 않는다. 실패해도 조용히 넘어간다.
        pass
