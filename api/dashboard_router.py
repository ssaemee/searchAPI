"""
대시보드 API Router
"""
from fastapi import APIRouter, HTTPException

from config import logger
from api.schema.aggs_request import AggsRequest
from api.schema.aggs_response import TotalCountResponse, AggsResponse
from service.dashboard.aggs_service import AggsService


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
service = AggsService()


@router.get("/total", response_model=TotalCountResponse)
def get_total_count() -> TotalCountResponse:
    """전체 회사 수 조회"""
    try:
        logger.info("[집계] 전체 회사 수 조회")
        result = service.get_total_count()
        logger.info(f"[집계] 전체 회사 수: {result.total}")
        return result
    except Exception as e:
        logger.error(f"[집계] 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/aggs", response_model=AggsResponse, response_model_exclude_none=True)
def get_aggs(request: AggsRequest) -> AggsResponse:
    """
    집계 조회 (옵션에 따라 국가별/연도별 선택)
    
    - include_country=true: 국가별 집계 포함 (회사 수 + 지난주 주가 평균)
    - include_year=true: 연도별 집계 포함 (회사 수 + 회사 분류 분포도)
    - 둘 다 true: 모두 포함
    - 둘 다 false: total만 반환
    """
    try:
        logger.info(
            f"[집계] include_country={request.include_country}, "
            f"include_year={request.include_year}"
        )
        result = service.get_aggs(request)
        logger.info(f"[집계] 결과: total={result.total}")
        return result
    except Exception as e:
        logger.error(f"[집계] 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))
