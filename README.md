# 경비 정산 시스템 (실습용)

「Claude Code 기반 AI Agent 개발 자동화 실무」 과정의 실습 저장소입니다.

경비 청구 내역을 사내 경비 규정에 따라 검증하고 결과를 표로 보여 주는 Python 애플리케이션입니다. 수강생은 이 저장소 위에 `.claude/` 하네스를 직접 구축합니다.

## 이 저장소의 상태

**클래스 이름만 있고 본문은 비어 있습니다.** 무엇을 어디에 만들지는 정해져 있고, 내용은 실습에서 직접 만듭니다.

| 폴더 | 내용 |
|---|---|
| `docs/` | 만들어야 할 것을 정한 문서 세 개 |
| `src/` | 클래스와 메서드 이름만 있는 골격. 본문은 비어 있습니다 |
| `tests/` | 테스트 데이터. 테스트 코드는 실습에서 만듭니다 |
| `samples/` | 부서별 경비 청구 파일 |

문서는 이 순서로 읽으세요.

| 문서 | 내용 |
|---|---|
| [`docs/요구사항.md`](docs/요구사항.md) | 무엇을 만드는지. 처리 흐름, 프로젝트 구조, 계약 |
| [`docs/데이터-스키마.md`](docs/데이터-스키마.md) | 청구 파일의 형식과 도메인 모델 넷의 속성 |
| [`docs/경비규정.md`](docs/경비규정.md) | 검증할 규정 20개 |

`src/` 의 클래스와 메서드 이름은 바꾸지 마세요. 이후 실습과 강의 중 예제가 이 이름을 씁니다. 규칙 파일은 없으므로 `src/core/domain/rules/` 아래에 직접 만듭니다.

## 준비

Windows PowerShell 기준입니다. Git, Node.js, Claude Code, uv 설치는 과정 챕터 2에서 안내합니다.

```powershell
git clone https://github.com/hagyutae/expense-settlement-lab.git C:\lgcns-lab
cd C:\lgcns-lab
uv sync
```

`uv sync` 가 Python 인터프리터와 패키지를 함께 설치합니다. Python을 따로 설치하지 않아도 됩니다.

## 실행

```powershell
uv run settle samples\연구소.csv
```

본문이 비어 있으므로 처음에는 아무것도 출력하지 않고 끝납니다. 챕터 3에서 첫 규칙을 만들면 결과 표가 나오기 시작합니다.

## 테스트

```powershell
uv run pytest
```

처음에는 `no tests ran` 이 나옵니다. 테스트를 하나 만들 때마다 통과 건수가 올라갑니다.

## 브랜치

| 브랜치 | 내용 |
|---|---|
| `main` | 실습 시작 상태입니다. 여기서 시작하세요 |
| `chapter-3` ~ `chapter-7` | 해당 챕터를 마친 상태입니다 |
| `rules-only` | 규칙만 완성된 상태입니다. 하네스는 없습니다 |
| `solution` | 전체 완성본입니다 |

진도를 따라가지 못했을 때 해당 챕터 브랜치로 이동해 이어서 진행하세요.

```powershell
git stash
git switch chapter-4
```

## 안내

`samples/` 폴더의 카드번호, 계좌번호, 주민등록번호는 모두 실습을 위해 생성한 가짜 데이터입니다. 실제 개인정보가 아닙니다.
