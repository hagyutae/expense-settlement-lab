---
description: 아직 구현하지 않은 규칙 코드를 확인합니다
allowed-tools: Bash(grep:*), Bash(ls:*)
---

규정에 실린 규칙:
!`grep "^### R" docs/경비규정.md`

구현된 규칙 파일:
!`ls src/core/domain/rules`

두 목록을 대조해 아직 구현하지 않은 규칙만 알려 주세요.
`코드 · 이름 · 유형` 형식으로 한 줄씩 적고, 마크다운 제목 표시는 떼어 냅니다.
다른 설명은 덧붙이지 않습니다.
