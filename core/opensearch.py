"""
OpenSearch 클라이언트 모듈
"""
import os
from typing import Generator
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk
from dotenv import load_dotenv


class OpenSearchClient:
    """opensearch 클라이언트 (자동 재연결)"""
    
    def __init__(self):
        load_dotenv()
        self.client = None
    
    def create_client(self) -> OpenSearch:
        """opensearch 클라이언트 생성"""
        return OpenSearch(
            hosts=[{
                'host': os.getenv('OPENSEARCH_HOST', 'localhost'),
                'port': int(os.getenv('OPENSEARCH_PORT', 9200))
            }],
            http_auth=(
                os.getenv('OPENSEARCH_USERNAME', 'admin'),
                os.getenv('OPENSEARCH_PASSWORD')
            ),
            use_ssl=os.getenv('OPENSEARCH_USE_SSL', 'true').lower() == 'true',
            verify_certs=False,
            ssl_show_warn=False,
            timeout=30
        )
    
    def get_client(self) -> OpenSearch:
        """연결 확인 후 클라이언트 반환 (필요시 재연결)"""
        if self.client is None or not self.ping():
            self.client = self.create_client()
        return self.client
    
    def ping(self) -> bool:
        """연결 상태 확인"""
        if self.client is None:
            return False
        try:
            return self.client.ping()
        except Exception:
            return False
    
    def info(self) -> dict:
        """클러스터 정보"""
        return self.get_client().info()
    
    def cluster_health(self) -> dict:
        """클러스터 헬스 확인"""
        return self.get_client().cluster.health()
    
    def get_nodes(self) -> list:
        """노드 목록"""
        return self.get_client().cat.nodes(format='json')
    
    def index_exists(self, index_name: str) -> bool:
        """인덱스 존재 확인"""
        return self.get_client().indices.exists(index=index_name)
    
    def create_index(self, index_name: str, body: dict) -> dict:
        """인덱스 생성"""
        return self.get_client().indices.create(index=index_name, body=body)
    
    def delete_index(self, index_name: str) -> dict:
        """인덱스 삭제"""
        if self.index_exists(index_name):
            return self.get_client().indices.delete(index=index_name)
        return {
            "acknowledged": True,
            "message": "Index does not exist"
        }
    
    def refresh_index(self, index_name: str) -> dict:
        """인덱스 리프레시"""
        return self.get_client().indices.refresh(index=index_name)
    
    def search(self, index_name: str, body: dict) -> dict:
        """검색 실행"""
        return self.get_client().search(index=index_name, body=body)
    
    def count(self, index_name: str) -> int:
        """문서 수 조회"""
        result = self.get_client().count(index=index_name)
        return result['count']
    
    def bulk_insert(self, actions: Generator) -> tuple:
        """벌크 삽입"""
        return bulk(
            self.get_client(),
            actions,
            raise_on_error=False,
            stats_only=False
        )
