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
tests/input/ output/ usecase/   계층별 테스트
ui/                   React 화면. API 를 호출할 뿐 src/ 와 섞지 않습니다
docs/                 규정과 명세
```

## 코딩 컨벤션

- 구현체는 `src/application/container.py` 와 `tests/container.py` 에서 조립합니다.
- 규칙은 나열하지 않습니다. 규칙 클래스에 `@rule` 을 붙이면 `load_rules()` 가 모읍니다. 규칙 파일을 추가하는 것으로 끝입니다.
- 집계는 `Aggregator` 를 상속하고 `core/service/usecase/aggregate/` 에 둡니다. 출력 계층은 어떤 집계가 있는지 알지 못합니다.
- 반올림은 계산 계층에서 한 번만 합니다.

### 금지

- 카드번호, 계좌번호, 주민등록번호를 로그나 출력에 남기지 않습니다. 청구ID와 파일 경로까지만 남깁니다.
