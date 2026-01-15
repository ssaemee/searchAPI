"""
집계 응답 스키마
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class TotalCountResponse(BaseModel):
    """전체 개수 응답"""
    total: int = Field(description="전체 회사 수")


class CountryAggItem(BaseModel):
    """국가별 집계 아이템"""
    country: str = Field(description="국가")
    company_count: int = Field(description="회사 수")
    avg_last_week_stock: float = Field(description="지난주 주가 평균")


class CompanyTypeCount(BaseModel):
    """회사 분류별 개수"""
    company_type: str = Field(description="회사 분류")
    company_count: int = Field(description="회사 수")


class YearAggItem(BaseModel):
    """연도별 집계 아이템"""
    year: int = Field(description="연도")
    company_count: int = Field(description="회사 수")
    company_type_distribution: List[CompanyTypeCount] = Field(description="회사 분류 분포도")


class AggsResponse(BaseModel):
    """집계 응답"""
    total: int = Field(description="전체 회사 수")
    country_aggs: Optional[List[CountryAggItem]] = Field(
        default=None,
        description="국가별 집계 데이터 (include_country=true일 때)"
    )
    year_aggs: Optional[List[YearAggItem]] = Field(
        default=None,
        description="연도별 집계 데이터 (include_year=true일 때)"
    )
