"""API 응답 모델.

화면과 맺는 계약입니다. 여기 적은 필드가 그대로 `/openapi.json` 이 되고,
Swagger 화면과 React 화면이 이 정의를 봅니다.

`core` 의 도메인 객체를 그대로 내보내지 않습니다. 도메인이 바뀌어도
계약이 따라 흔들리지 않게 하려고 응답 전용 모델을 따로 둡니다.
"""

from pydantic import BaseModel, Field


class Violation(BaseModel):
    code: str = Field(description="규칙 코드", examples=["R021"])
    name: str = Field(description="규칙 이름", examples=["교육훈련비 사전승인"])
    message: str = Field(
        description="위반 내용",
        examples=["20만원을 초과하는 교육훈련비는 사전승인 번호가 필요합니다"],
    )


class Judgement(BaseModel):
    claim_id: str = Field(description="청구ID", examples=["EXP-2026-0266"])
    employee_name: str = Field(description="성명", examples=["최수아"])
    department: str = Field(description="부서", examples=["개발2팀"])
    used_date: str = Field(description="사용일자. 원본 문자열 그대로", examples=["2026-06-24"])
    expense_type: str = Field(description="계정과목", examples=["교육훈련비"])
    amount: int | None = Field(
        description="금액. 숫자로 읽히지 않으면 null", examples=[450000]
    )
    is_passed: bool = Field(description="위반이 하나도 없으면 참", examples=[False])
    violations: list[Violation] = Field(description="위반 목록. 규칙 코드 순")


class Summary(BaseModel):
    total: int = Field(description="전체 청구 건수", examples=[45])
    passed: int = Field(description="통과 건수", examples=[37])
    rejected: int = Field(description="반려 건수", examples=[8])


class AggregationTable(BaseModel):
    name: str = Field(description="표 제목", examples=["부서별 정산 요약"])
    columns: list[str] = Field(
        description="열 이름",
        examples=[["부서", "청구", "통과", "반려", "반려율", "청구금액", "반려금액"]],
    )
    rows: list[list] = Field(
        description="행. columns 순서를 따른다",
        examples=[[["개발2팀", 45, 37, 8, 17.8, 3333500, 786000]]],
    )


class SettlementResponse(BaseModel):
    summary: Summary = Field(description="건수 요약")
    judgements: list[Judgement] = Field(
        description="청구 건별 판정. 파일의 행 순서를 유지한다"
    )
    aggregations: list[AggregationTable] = Field(description="집계 표 목록")


class ErrorResponse(BaseModel):
    detail: str = Field(
        description="오류 내용",
        examples=["지원하지 않는 입력 형식입니다: xlsx (가능: csv, md)"],
    )
