"""
집계 요청 스키마
"""
from pydantic import BaseModel, Field


class AggsRequest(BaseModel):
    """집계 요청 (국가별/연도별 선택)"""
    include_country: bool = Field(
        default=True,
        description="국가별 집계 포함 여부"
    )
    include_year: bool = Field(
        default=True,
        description="연도별 집계 포함 여부"
    )
