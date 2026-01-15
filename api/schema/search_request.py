"""
검색 요청 스키마
"""
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class SearchKeyword(BaseModel):
    """검색어 스키마"""
    type: Literal["company_name", "drug_name", "indication"] = Field(
        description="검색 타입: company_name, drug_name, indication"
    )
    keyword: str = Field(description="검색 키워드")


class FilterSchema(BaseModel):
    """필터 스키마"""
    country: Optional[List[str]] = Field(
        default=[],
        description="국가 필터"
    )
    company_type: Optional[List[str]] = Field(
        default=[],
        description="회사 분류 필터"
    )
    stage: Optional[List[str]] = Field(
        default=[],
        description="파이프라인 단계 필터"
    )
    search: Optional[SearchKeyword] = Field(None, description="검색어")


class OrderSchema(BaseModel):
    """정렬 스키마"""
    sortBy: Literal[
        "company_name",
        "now_stock_price",
        "last_week_stock_price"
    ] = Field(description="정렬 기준")
    sortOrder: Literal["asc", "desc"] = Field(default="asc", description="정렬 순서")


class SearchRequest(BaseModel):
    """검색 요청 스키마"""
    page: int = Field(default=1, ge=1, description="페이지 번호")
    size: int = Field(default=20, ge=1, le=100, description="페이지당 개수")
    filter: Optional[FilterSchema] = Field(default=None, description="필터")
    order: Optional[List[OrderSchema]] = Field(default=[], description="정렬")
