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

- 구현체는 `src/application/container.py` 와 `tests/container.py` 에서 조립합니다. 두 곳 모두에 등록해야 실행 결과와 테스트 결과가 일치합니다.

### 금지

- 카드번호, 계좌번호, 주민등록번호를 로그나 출력에 남기지 않습니다. 청구ID와 파일 경로까지만 남깁니다.
