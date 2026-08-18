# 경비 정산 시스템

사내 경비 규정에 따라 경비 청구를 검사하는 프로그램입니다.

## 기술 스택

- Python 3.12 이상을 씁니다.
- uv 로 패키지와 가상환경을 관리합니다. 실행은 `uv run` 으로 시작합니다.
- pytest. `pythonpath` 는 `src` 입니다.

## 폴더 구조

```
src/core/domain/      모델과 규칙. 바깥 계층을 모릅니다
src/core/service/     입력 · 처리 · 출력. 계층마다 base.py 에 추상 클래스가 있습니다
src/application/      조립과 진입점
tests/rules/          규칙별 테스트와 픽스처
tests/golden/         골든 데이터. 수정하지 않습니다
docs/                 규정과 명세
```

## 코딩 컨벤션

### 규칙 추가

- 규칙 파일은 `src/core/domain/rules/rXXX_영문설명.py` 로 만듭니다.
- 단건 규칙은 `RowRule`, 다건 규칙은 `BatchRule` 을 상속합니다. 어느 쪽인지는 규정 항목 제목에 적혀 있습니다.
- `code` 와 `name` 은 규정 항목 제목에서 그대로 가져옵니다.
- 테스트는 `tests/rules/test_rXXX.py` 에 만들고 픽스처 `tests/rules/fixtures/rXXX.csv` 를 씁니다.
- **등록은 두 곳입니다.** `src/application/container.py` 의 `build_service` 와 `tests/container.py` 의 `all_rules` 입니다. 한 곳만 하면 실행 결과와 테스트 결과가 어긋납니다.

새 규칙은 @src/core/domain/rules/r001_required_fields.py 의 구조를 따릅니다.

판정 조건과 위반 문구는 규정 문서를 그대로 따릅니다.

@docs/경비규정.md

데이터 속성 이름은 `docs/데이터-스키마.md` 에 있습니다. 규칙마다 보는 문서가 아니므로
경로만 적습니다.

### 금지

- 카드번호, 계좌번호, 주민등록번호를 로그나 출력에 남기지 않습니다. 청구ID와 파일 경로까지만 남깁니다.
