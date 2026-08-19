"""웹 진입점.

    uv run uvicorn application.web.main:app --host 127.0.0.1 --port 8000

CLI와 형제입니다. 조립은 각자 부르고 `core` 는 어느 쪽도 알지 못합니다.
판정 결과를 직렬화해 내려주므로 출력 계층을 거치지 않습니다.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application.web.routes import router

app = FastAPI(
    title="경비 정산 API",
    description="경비 청구 파일을 올리면 사내 경비 규정으로 판정하고 요약과 집계를 함께 돌려줍니다.",
    version="1.0.0",
)

# 개발 중 Vite 화면이 다른 포트에서 뜬다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
