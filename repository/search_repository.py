"""
검색 Repository
"""
from typing import Optional, List

from config import logger
from core.opensearch import OpenSearchClient
from api.schema.search_request import SearchRequest, FilterSchema, OrderSchema


class SearchRepository:
    """OpenSearch 검색 Repository"""
    
    def __init__(self):
        self.os = OpenSearchClient()
        self.index_name = 'companies'
    
    def search(self, request: SearchRequest) -> dict:
        """검색 실행"""
        query = self.build_query(request)
        logger.info(f"[Repository] 검색 쿼리: {query}")
        
        result = self.os.search(self.index_name, query)
        hits_count = len(result.get('hits', {}).get('hits', []))
        logger.info(f"[Repository] 검색 결과: {hits_count}건")
        
        return result
    
    def build_query(self, request: SearchRequest) -> dict:
        """전체 쿼리 빌드"""
        has_search = self.has_search_keyword(request)
        
        return {
            "from": (request.page - 1) * request.size,
            "size": request.size,
            "query": self.build_bool_query(request),
            "sort": self.build_sort(request.order, has_search)
        }
    
    def has_search_keyword(self, request: SearchRequest) -> bool:
        """검색어 유무 확인"""
        if request.filter is None:
            return False
        if request.filter.search is None:
            return False
        return True
    
    def build_bool_query(self, request: SearchRequest) -> dict:
        """bool 쿼리 구성"""
        if not request.filter:
            return {"match_all": {}}
        
        must = []
        filters = []
        
        # 일반 검색 (match 쿼리)
        if request.filter.search:
            search_query = self.build_search_query(request.filter.search)
            if search_query:
                must.append(search_query)
        
        # 필터 (term 쿼리)
        filters = self.build_filter_queries(request.filter)
        
        # must, filter 둘 다 비어있으면 match_all
        if not must and not filters:
            return {"match_all": {}}
        
        # bool 쿼리 구성
        bool_query = {"bool": {}}
        if must:
            bool_query["bool"]["must"] = must
        if filters:
            bool_query["bool"]["filter"] = filters
        
        return bool_query
    
    def build_search_query(self, search) -> Optional[dict]:
        """일반 검색 쿼리 빌드 (match)"""
        if not search or not search.keyword:
            return None
        
        keyword = search.keyword
        
        # 회사명 검색
        if search.type == "company_name":
            return {"match": {"company_name": keyword}}
        
        # 약물명 검색 (nested)
        if search.type == "drug_name":
            return self.build_nested_match("main_pipeline.drug_name", keyword)
        
        # 적응증 검색 (nested)
        if search.type == "indication":
            return self.build_nested_match("main_pipeline.indication", keyword)
        
        return None
    
    def build_nested_match(self, field: str, keyword: str) -> dict:
        """nested match 쿼리 생성"""
        return {
            "nested": {
                "path": "main_pipeline",
                "query": {
                    "match": {field: keyword}
                }
            }
        }
    
    def build_filter_queries(self, filter_schema: FilterSchema) -> list:
        """필터 쿼리 빌드 (term)"""
        filters = []
        
        # 국가 필터
        if filter_schema.country:
            filters.append({"terms": {"country": filter_schema.country}})
        
        # 회사 분류 필터
        if filter_schema.company_type:
            filters.append({"terms": {"company_type": filter_schema.company_type}})
        
        # 파이프라인 단계 필터 (nested)
        if filter_schema.stage:
            filters.append({
                "nested": {
                    "path": "main_pipeline",
                    "query": {
                        "terms": {"main_pipeline.stage": filter_schema.stage}
                    }
                }
            })
        
        return filters
    
    def build_sort(self, order: Optional[List[OrderSchema]], has_search: bool) -> list:
        """정렬 조건 빌드"""
        # 사용자가 정렬 조건을 지정한 경우
        if order:
            sort_list = []
            for o in order:
                field = o.sortBy
                if field == "company_name":
                    field = "company_name.keyword"
                sort_list.append({field: {"order": o.sortOrder}})
            return sort_list
        
        # 검색어가 있으면 스코어 내림차순
        if has_search:
            return [{"_score": {"order": "desc"}}]
        
        # 검색어가 없으면 회사명 오름차순
        return [{"company_name.keyword": {"order": "asc"}}]
