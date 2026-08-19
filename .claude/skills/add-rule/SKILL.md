---
name: add-rule
description: 경비 규정의 규칙 코드를 받아 규칙 구현, 테스트 작성, 컨테이너 등록까지 처리합니다. 규칙을 추가할 때 사용합니다.
allowed-tools: Bash(uv run python ${CLAUDE_SKILL_DIR}/scripts/check_rule.py:*)
---

# 규칙 추가

규칙 코드를 받아 아래를 모두 마친다. 코드를 여러 개 받으면 코드마다 되풀이한다.

대상 규칙: $ARGUMENTS

## 절차

1. 아래 규정에서 해당 코드의 항목을 찾아 판정 조건과 위반 문구를 확인한다.
2. `src/core/domain/rules/rXXX_영문설명.py` 에 규칙을 만들고 클래스에 `@rule` 을 붙인다.
3. `tests/rules/test_rXXX.py` 를 만든다. 픽스처 `tests/rules/fixtures/rXXX.csv` 가 없으면 함께 만든다.
4. `uv run python ${CLAUDE_SKILL_DIR}/scripts/check_rule.py <규칙 코드>` 로 규칙 구현·테스트·픽스처·레지스트리 등록이 모두 반영됐는지 확인한다. **경로를 줄이지 말고 위에 적힌 그대로 실행한다.** 빠진 곳이 있으면 채우고 다시 돌린다.
5. `uv run pytest` 로 전체가 통과하는지 확인한다.

## 규약

- 단건 규칙은 `RowRule`, 다건 규칙은 `BatchRule` 을 상속한다. 어느 쪽인지는 규정 항목 제목에 적혀 있다.
- **조립 파일은 고치지 않는다.** `@rule` 이 붙어 있으면 `load_rules()` 가 앱과 테스트 양쪽에 넣어 준다.
- `code` 와 `name` 은 규정 항목 제목에서 그대로 가져온다.
- 판정 조건과 위반 문구는 규정을 그대로 따른다. 임의로 바꾸지 않는다.
- 구현 구조는 @src/core/domain/rules/r001_required_fields.py 를 따른다.
- 데이터 속성 이름은 `docs/데이터-스키마.md` 에 있다.

## 규정

@docs/경비규정.md
