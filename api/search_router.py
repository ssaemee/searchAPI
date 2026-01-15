"""
검색 API Router
"""
from fastapi import APIRouter, HTTPException

from config import logger
from api.schema.search_request import SearchRequest
from api.schema.search_response import SearchResponse
from service.search.search_service import SearchService


router = APIRouter(prefix="/search", tags=["Search"])
service = SearchService()


@router.post("/companies", response_model=SearchResponse)
def search_companies(request: SearchRequest) -> SearchResponse:
    """
    회사 검색 API
    
    - 일반 검색: 회사명, 약물명, 적응증
    - 필터: 국가, 회사 분류, 파이프라인 단계
    - 정렬: 회사명, 주가
    """
    try:
        logger.info(f"[검색] page={request.page}, size={request.size}")
        
        if request.filter and request.filter.search:
            logger.info(
                f"[검색] type={request.filter.search.type}, "
                f"keyword={request.filter.search.keyword}"
            )
        
        result = service.search(request)
        logger.info(f"[검색] 결과: total={result.total}")
        
        return result
    except Exception as e:
        logger.error(f"[검색] 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))
