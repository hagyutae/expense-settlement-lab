# 경비 정산 시스템 (실습용)

「Claude Code 기반 AI Agent 개발 자동화 실무」 과정의 실습 저장소입니다.

CSV·XLSX로 올라온 경비 청구 내역을 사내 경비 규정에 따라 검증하고, 결과를 화면에 표로 보여 주는 Flask 애플리케이션입니다. 수강생은 이 저장소 위에 하루 동안 `.claude/` 하니스를 직접 쌓아 올립니다.

## 준비

Windows PowerShell 기준입니다. Git, Node.js, Claude Code, uv 설치는 과정 모듈 2에서 안내합니다.

```powershell
git clone https://github.com/hagyutae/expense-settlement-lab.git C:\lgcns-lab
cd C:\lgcns-lab
uv sync
.\.venv\Scripts\Activate.ps1
```

`uv sync`가 Python 인터프리터와 패키지를 함께 설치합니다. Python을 따로 설치하지 않아도 됩니다.

## 실행

```powershell
uv run python -m src.app
```

브라우저에서 `http://127.0.0.1:5000` 으로 접속합니다.

## 테스트

```powershell
uv run pytest
```

## 브랜치

| 브랜치 | 내용 |
|---|---|
| `main` | 실습 시작 상태입니다. 여기서 시작하세요 |
| `checkpoint/module-4` | 모듈 4까지 완료한 상태입니다 |
| `checkpoint/module-5` | 모듈 5까지 완료한 상태입니다 |
| `checkpoint/module-6` | 모듈 6까지 완료한 상태입니다 |
| `solution` | 전체 완성본입니다 |

진도를 따라가지 못했을 때 해당 체크포인트로 이동해 이어서 진행하세요.

```powershell
git checkout checkpoint/module-4
```

## 안내

`samples/` 폴더의 카드번호, 계좌번호, 주민등록번호는 모두 실습을 위해 생성한 가짜 데이터입니다. 실제 개인정보가 아닙니다.
