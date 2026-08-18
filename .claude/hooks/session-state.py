"""세션이 시작될 때 작업 환경의 상태를 넣어 준다.

git 상태와 테스트 결과는 세션마다 다르므로 CLAUDE.md 에 적어 둘 수 없다.
"""

import json
import subprocess


def run(*command):
    try:
        done = subprocess.run(command, capture_output=True, text=True, timeout=120)
        return done.stdout.strip()
    except Exception:
        return ""


def changed_files(limit=3):
    """파일이 많을 때 목록을 통째로 넣으면 세션마다 컨텍스트를 크게 먹는다."""
    # 각 줄은 "상태 경로" 형태다. 앞의 상태 표시를 떼고 경로만 남긴다.
    files = [line.split(maxsplit=1)[-1] for line in run("git", "status", "--short").splitlines()]
    if not files:
        return "없음"
    if len(files) > limit:
        return f"{', '.join(files[:limit])} 외 {len(files) - limit}개"
    return ", ".join(files)


tested = run("uv", "run", "pytest", "-q", "--no-header")

state = "\n".join([
    f"최근 커밋: {run('git', 'log', '-1', '--oneline')}",
    f"변경된 파일: {changed_files()}",
    f"테스트: {tested.splitlines()[-1] if tested else '실행하지 못했습니다'}",
])

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": state,
    }
}, ensure_ascii=False))
