"""
OpenSearch 인덱스 생성 및 데이터 로드
"""
from scripts.create_index import create_index
from scripts.load_data import load_excel_to_opensearch
from core.opensearch import OpenSearchClient
from config import MOCK_DATA, logger


def setup_connection():
    """OpenSearch 연결 확인"""
    os = OpenSearchClient()
    info = os.info()
    health = os.cluster_health()
    
    logger.info(f"클러스터: {info['cluster_name']}")
    logger.info(f"버전: {info['version']['number']}")
    logger.info(f"상태: {health['status']}")
    logger.info(f"노드: {health['number_of_nodes']}개")
    
    return os


def setup_index(os_client):
    """인덱스 생성"""
    result = create_index(os_client, index_name='companies')
    
    if result:
        logger.info("인덱스 생성 완료")
    else:
        logger.error("인덱스 생성 실패")
    
    return result


def setup_data():
    """데이터 로드"""
    result = load_excel_to_opensearch(str(MOCK_DATA))
    
    if result:
        logger.info("데이터 로드 완료")
    else:
        logger.error("데이터 로드 실패")
    
    return result


def verify_data(os_client):
    """데이터 검증"""
    result = os_client.search('companies', {
        "size": 1,
        "query": {"match_all": {}}
    })
    
    hits = result['hits']['hits']
    if hits:
        doc = hits[0]['_source']
        logger.info(f"샘플: {doc['company_name']} ({doc['country']})")
        return True
    return False


def main():
    logger.info("=== OpenSearch 인덱스 설정 ===")
    
    try:
        # 1. 연결 확인
        os_client = setup_connection()
        
        # 2. 인덱스 생성
        if not setup_index(os_client):
            return False
        
        # 3. 데이터 로드
        if not setup_data():
            return False
        
        # 4. 검증
        if not verify_data(os_client):
            return False
        
        logger.info("=== 설정 완료 ===")
        return True
        
    except Exception as e:
        logger.error(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
