"""
집계 Repository
"""
from config import logger
from core.opensearch import OpenSearchClient


class AggsRepository:
    """OpenSearch 집계 Repository"""
    
    def __init__(self):
        self.os = OpenSearchClient()
        self.index_name = 'companies'
    
    def get_aggs(self, include_country: bool = True, include_year: bool = True) -> dict:
        """
        집계 조회 (옵션에 따라 국가별/연도별 선택)
        """
        logger.info(
            f"[Repository] 집계 요청: country={include_country}, year={include_year}"
        )
        
        aggs = {}
        
        # 국가별 집계
        if include_country:
            aggs["by_country"] = {
                "terms": {
                    "field": "country",
                    "size": 50
                },
                "aggs": {
                    "avg_last_week_stock": {
                        "avg": {
                            "field": "last_week_stock_price"
                        }
                    }
                }
            }
        
        # 연도별 집계
        if include_year:
            aggs["by_founded_year"] = {
                "date_histogram": {
                    "field": "founded_date",
                    "calendar_interval": "year",
                    "format": "yyyy",
                    "min_doc_count": 1
                },
                "aggs": {
                    "company_type_distribution": {
                        "terms": {
                            "field": "company_type",
                            "size": 20
                        }
                    }
                }
            }
        
        query = {
            "size": 0,
            "track_total_hits": True,
            "query": {
                "match_all": {}
            },
            "aggs": aggs
        }
        
        result = self.os.search(self.index_name, query)
        total = result.get('hits', {}).get('total', {}).get('value', 0)
        logger.info(f"[Repository] 집계 결과: total={total}")
        
        return result
