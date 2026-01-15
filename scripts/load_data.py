"""
Excel 데이터를 OpenSearch에 로드하는 스크립트
"""
import re

import pandas as pd

from config import MOCK_DATA, logger
from core.opensearch import OpenSearchClient


def parse_pipeline(pipeline_str):
    """
    파이프라인 문자열을 파싱하여 리스트로 변환
    예: "[ZL-6129 (Osteoporosis, Phase 3), DX-4259 (Atrial Fibrillation, Phase 2)]"
    """
    if pd.isna(pipeline_str) or not pipeline_str:
        return []
    
    # 대괄호 제거
    pipeline_str = pipeline_str.strip('[]').strip()
    
    # 각 항목을 "), " 기준으로 분리
    items = re.split(r'\),\s*', pipeline_str)
    
    pipelines = []
    for item in items:
        # 각 항목에서 "약물명 (적응증, 단계)" 파싱
        match = re.match(r'([^(]+)\s*\(([^,]+),\s*([^)]+)\)?', item.strip())
        if match:
            drug_name = match.group(1).strip()
            indication = match.group(2).strip()
            stage = match.group(3).strip()
            
            pipelines.append({
                "drug_name": drug_name,
                "indication": indication,
                "stage": stage
            })
    
    return pipelines


def prepare_document(row):
    """DataFrame 행을 OpenSearch 문서로 변환"""
    doc = {
        "id": int(row['ID']),
        "company_name": str(row['회사명']),
        "country": str(row['국가']),
        "company_type": str(row['회사 분류']),
        "last_week_stock_price": float(row['지난주 주가']),
        "now_stock_price": float(row['실시간 주가'])
    }
    
    # 날짜 변환
    try:
        if pd.notna(row['설립 날짜']):
            founded_date = pd.to_datetime(row['설립 날짜'])
            doc['founded_date'] = founded_date.strftime('%Y.%m.%d')
    except Exception as e:
        logger.warning(f"날짜 변환 오류 (ID: {row['ID']}): {e}")
    
    # 파이프라인 파싱
    pipeline_str = row['주요 파이프라인\n약물명 (적응증, 단계)']
    doc['main_pipeline'] = parse_pipeline(pipeline_str)
    
    return doc


def generate_actions(df, index_name='companies'):
    """Bulk API용 액션 생성"""
    for idx, row in df.iterrows():
        doc = prepare_document(row)
        yield {
            "_index": index_name,
            "_id": doc['id'],
            "_source": doc
        }


def load_excel_to_opensearch(excel_path, index_name='companies'):
    """Excel 데이터를 OpenSearch에 로드"""
    os_client = OpenSearchClient()
    
    # Excel 파일 읽기
    logger.info(f"Excel 파일 읽는 중: {excel_path}")
    df = pd.read_excel(excel_path)
    logger.info(f"총 {len(df)}개 행 로드됨")
    
    # 인덱스 존재 확인
    if not os_client.index_exists(index_name):
        logger.error(f"인덱스 '{index_name}'가 존재하지 않습니다.")
        logger.info("먼저 'python -m scripts.create_index'를 실행하세요.")
        return False
    
    # Bulk 인덱싱
    logger.info(f"데이터를 '{index_name}' 인덱스에 로드 중...")
    success, failed = os_client.bulk_insert(generate_actions(df, index_name))
    
    logger.info(f"로드 완료 - 성공: {success}개")
    if failed:
        logger.warning(f"실패: {len(failed)}개")
    
    # 인덱스 리프레시
    os_client.refresh_index(index_name)
    
    # 결과 확인
    count = os_client.count(index_name)
    logger.info(f"현재 인덱스 문서 수: {count}개")
    
    return True


def main():
    try:
        excel_path = MOCK_DATA
        
        if not excel_path.exists():
            logger.error(f"Excel 파일을 찾을 수 없습니다: {excel_path}")
            return False
        
        load_excel_to_opensearch(str(excel_path))
        
        logger.info("데이터 로드가 완료되었습니다.")
        
    except Exception as e:
        logger.error(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    main()
