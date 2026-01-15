"""
검색 응답 스키마
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class PipelineInfo(BaseModel):
    """파이프라인 정보"""
    drug_name: str = Field(description="약물명")
    indication: str = Field(description="적응증")
    stage: str = Field(description="단계")


class CompanyData(BaseModel):
    """회사 데이터"""
    id: int = Field(description="회사 ID")
    company_name: str = Field(description="회사명")
    founded_date: Optional[str] = Field(None, description="설립일 (yyyy.MM.dd)")
    country: str = Field(description="국가")
    company_type: str = Field(description="회사 분류")
    last_week_stock_price: float = Field(description="지난주 주가")
    now_stock_price: float = Field(description="실시간 주가")
    main_pipeline: List[PipelineInfo] = Field(default=[], description="주요 파이프라인")


class SearchResponse(BaseModel):
    """검색 응답 스키마"""
    page: int = Field(description="현재 페이지")
    size: int = Field(description="페이지당 개수")
    totalPages: int = Field(description="전체 페이지 수")
    total: int = Field(description="전체 검색 결과 수")
    data: List[CompanyData] = Field(description="회사 데이터 리스트")

