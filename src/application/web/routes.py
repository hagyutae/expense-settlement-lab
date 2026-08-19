"""HTTP 경로.

조립은 진입점이 부릅니다. `core` 는 여기까지 알지 못합니다.
"""

from fastapi import APIRouter, HTTPException, UploadFile

from application.container import build_loader, build_service
from application.web.schema import ErrorResponse, SettlementResponse
from application.web.serializer import to_response
from core.service.input.base import ENCODING

router = APIRouter(prefix="/api")


@router.post(
    "/settle",
    summary="청구 파일 판정",
    response_model=SettlementResponse,
    responses={400: {"model": ErrorResponse, "description": "형식이 다르거나 읽을 수 없는 파일"}},
)
async def settle(file: UploadFile):
    """청구 파일 하나를 받아 요약과 판정, 집계를 돌려줍니다.

    확장자로 입력 형식을 정합니다. `.csv` 와 `.md` 를 받습니다.
    """
    fmt = (file.filename or "").rsplit(".", 1)[-1].lower()
    try:
        loader = build_loader(fmt)
        expenses = loader.parse((await file.read()).decode(ENCODING))
    except (UnicodeDecodeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return to_response(build_service().settle(expenses))
