"""
OpenSearch 인덱스 생성 스크립트
"""
import json

from config import OPENSEARCH_SETTINGS, OPENSEARCH_MAPPINGS, logger
from core.opensearch import OpenSearchClient


def load_settings(settings_file=None):
    """설정 파일 로드"""
    if settings_file is None:
        settings_file = OPENSEARCH_SETTINGS
    with open(settings_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_mappings(mappings_file=None):
    """매핑 파일 로드"""
    if mappings_file is None:
        mappings_file = OPENSEARCH_MAPPINGS
    with open(mappings_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_index(os_client, index_name='companies'):
    """인덱스 생성"""
    # 인덱스가 이미 존재하면 삭제
    if os_client.index_exists(index_name):
        os_client.delete_index(index_name)
        logger.info(f"기존 인덱스 '{index_name}' 삭제")
    
    # 설정 및 매핑 파일 로드
    settings = load_settings()
    mappings = load_mappings()
    
    if index_name not in settings:
        logger.error(f"'{index_name}' 설정 정보를 찾을 수 없습니다.")
        return False
    
    if index_name not in mappings:
        logger.error(f"'{index_name}' 매핑 정보를 찾을 수 없습니다.")
        return False
    
    # 인덱스 생성 (settings + mappings 결합)
    body = {
        "settings": settings[index_name],
        "mappings": mappings[index_name]
    }
    
    os_client.create_index(index_name, body)
    logger.info(f"인덱스 '{index_name}' 생성 완료")
    logger.info(f"설정 파일: {OPENSEARCH_SETTINGS}")
    logger.info(f"매핑 파일: {OPENSEARCH_MAPPINGS}")
    
    return True


def main():
    try:
        os = OpenSearchClient()
        
        # 연결 확인
        info = os.info()
        logger.info(f"OpenSearch 연결 성공: {info['version']['number']}")
        
        # 인덱스 생성
        create_index(os, index_name='companies')
        
        logger.info("인덱스 생성이 완료되었습니다.")
        
    except Exception as e:
        logger.error(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    main()
