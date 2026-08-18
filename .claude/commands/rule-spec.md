---
description: 규칙 코드 하나의 규정 내용을 설명합니다
argument-hint: [규칙 코드]
allowed-tools: Bash(grep:*)
---

규정 문서에서 뽑은 부분입니다.

!`grep -A 16 "^### $ARGUMENTS " docs/경비규정.md`

위에서 $ARGUMENTS 항목만 골라 규칙 유형, 판정 조건, 위반 문구 세 줄로 정리해 주세요.
뒤따라 나온 다른 규칙 항목은 무시하고, 덧붙이는 설명은 적지 않습니다.
