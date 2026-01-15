"""
검색 Service
"""
import math
from typing import List

from config import logger
from api.schema.search_request import SearchRequest
from api.schema.search_response import SearchResponse, CompanyData, PipelineInfo
from repository.search_repository import SearchRepository


class SearchService:
    """검색 서비스"""
    
    def __init__(self):
        self.repository = SearchRepository()
    
    def search(self, request: SearchRequest) -> SearchResponse:
        """검색 실행 및 응답 변환"""
        logger.info(f"[Service] 검색 시작: page={request.page}, size={request.size}")
        
        # Repository 호출
        result = self.repository.search(request)
        
        # 응답 변환
        response = self.transform_response(result, request)
        logger.info(f"[Service] 검색 완료: total={response.total}, data={len(response.data)}건")
        
        return response
    
    def transform_response(self, result: dict, request: SearchRequest) -> SearchResponse:
        """opensearch 응답 → api 응답 변환"""
        hits = result.get('hits', {})
        total = hits.get('total', {}).get('value', 0)
        
        # 페이지 계산
        total_pages = math.ceil(total / request.size) if total > 0 else 0
        
        # 데이터 변환
        data = [self.transform_hit(hit) for hit in hits.get('hits', [])]
        
        return SearchResponse(
            page=request.page,
            size=request.size,
            totalPages=total_pages,
            total=total,
            data=data
        )
    
    def transform_hit(self, hit: dict) -> CompanyData:
        """개별 hit → CompanyData 변환"""
        source = hit.get('_source', {})
        
        # 파이프라인 변환
        pipelines = [
            PipelineInfo(
                drug_name=p.get('drug_name', ''),
                indication=p.get('indication', ''),
                stage=p.get('stage', '')
            )
            for p in source.get('main_pipeline', [])
        ]
        
        return CompanyData(
            id=source.get('id', 0),
            company_name=source.get('company_name', ''),
            founded_date=source.get('founded_date'),
            country=source.get('country', ''),
            company_type=source.get('company_type', ''),
            last_week_stock_price=source.get('last_week_stock_price', 0.0),
            now_stock_price=source.get('now_stock_price', 0.0),
            main_pipeline=pipelines
        )
