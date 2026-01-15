"""
집계 Service
"""
from typing import List, Optional

from config import logger
from api.schema.aggs_request import AggsRequest
from api.schema.aggs_response import (
    TotalCountResponse,
    AggsResponse, CountryAggItem,
    YearAggItem, CompanyTypeCount
)
from repository.aggs_repository import AggsRepository


class AggsService:
    """집계 서비스"""
    
    def __init__(self):
        self.repository = AggsRepository()
    
    def get_total_count(self) -> TotalCountResponse:
        """전체 회사 수 조회"""
        logger.info("[Service] 전체 회사 수 조회 시작")
        
        result = self.repository.get_aggs(include_country=False, include_year=False)
        total = self.extract_total(result)
        
        logger.info(f"[Service] 전체 회사 수: {total}")
        return TotalCountResponse(total=total)
    
    def get_aggs(self, request: AggsRequest) -> AggsResponse:
        """집계 조회 (옵션에 따라 국가별/연도별 선택)"""
        logger.info(
            f"[Service] 집계 시작: country={request.include_country}, "
            f"year={request.include_year}"
        )
        
        result = self.repository.get_aggs(
            include_country=request.include_country,
            include_year=request.include_year
        )
        
        total = self.extract_total(result)
        country_aggs = self.get_country_aggs(result, request.include_country)
        year_aggs = self.get_year_aggs(result, request.include_year)
        
        logger.info(f"[Service] 집계 완료: total={total}")
        
        return AggsResponse(
            total=total,
            country_aggs=country_aggs,
            year_aggs=year_aggs
        )
    
    def extract_total(self, result: dict) -> int:
        """전체 개수 추출"""
        return result.get('hits', {}).get('total', {}).get('value', 0)
    
    def get_country_aggs(self, result: dict, include: bool) -> Optional[List[CountryAggItem]]:
        """국가별 집계 조회"""
        if not include:
            return None
        
        country_aggs = self.transform_country_aggs(result)
        logger.info(f"[Service] 국가별 집계: {len(country_aggs)}개국")
        return country_aggs
    
    def get_year_aggs(self, result: dict, include: bool) -> Optional[List[YearAggItem]]:
        """연도별 집계 조회"""
        if not include:
            return None
        
        year_aggs = self.transform_year_aggs(result)
        logger.info(f"[Service] 연도별 집계: {len(year_aggs)}개년")
        return year_aggs
    
    def transform_country_aggs(self, result: dict) -> List[CountryAggItem]:
        """국가별 집계 변환"""
        buckets = result.get('aggregations', {}).get('by_country', {}).get('buckets', [])
        
        data = []
        for bucket in buckets:
            avg_value = bucket.get('avg_last_week_stock', {}).get('value')
            avg_stock = round(avg_value, 2) if avg_value is not None else 0.0
            
            data.append(CountryAggItem(
                country=bucket['key'],
                company_count=bucket['doc_count'],
                avg_last_week_stock=avg_stock
            ))
        
        return data
    
    def transform_year_aggs(self, result: dict) -> List[YearAggItem]:
        """연도별 집계 변환"""
        buckets = result.get('aggregations', {}).get('by_founded_year', {}).get('buckets', [])
        
        data = []
        for bucket in buckets:
            company_type_distribution = [
                CompanyTypeCount(
                    company_type=ct['key'],
                    company_count=ct['doc_count']
                )
                for ct in bucket.get('company_type_distribution', {}).get('buckets', [])
            ]
            
            data.append(YearAggItem(
                year=int(bucket['key_as_string']),
                company_count=bucket['doc_count'],
                company_type_distribution=company_type_distribution
            ))
        
        return data
