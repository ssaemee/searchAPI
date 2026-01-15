"""
FastAPI 메인 애플리케이션
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from config import logger
from api.search_router import router as search_router
from api.dashboard_router import router as dashboard_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 생명주기 관리
    
    - yield 전: 서버 시작 시 실행
    - yield 후: 서버 종료 시 실행
    """
    # 서버 시작
    logger.info("=== Search API 서버 시작 ===")
    yield
    # 서버 종료
    logger.info("=== Search API 서버 종료 ===")


app = FastAPI(
    title="Search/Aggs API",
    description="opensearch 기반 검색 및 집계 API",
    version="1.0.0",
    lifespan=lifespan
)

# 라우터 등록
app.include_router(search_router)
app.include_router(dashboard_router)


@app.get("/health")
def health_check():
    """헬스 체크"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

