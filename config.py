"""
프로젝트 설정
"""
from pathlib import Path
from core.logger import get_logger

# 루트 디렉토리
ROOT_DIR = Path(__file__).parent

# 로거
logger = get_logger("search_api")

# 하위 디렉토리
API_DIR = ROOT_DIR / 'api'
CORE_DIR = ROOT_DIR / 'core'
SCHEMA_DIR = ROOT_DIR / 'schema'
REPOSITORY_DIR = ROOT_DIR / 'repository'
SCRIPTS_DIR = ROOT_DIR / 'scripts'
SERVICE_DIR = ROOT_DIR / 'service'
TESTS_DIR = ROOT_DIR / 'tests'
LOGS_DIR = ROOT_DIR / 'logs'

# 파일 경로
OPENSEARCH_SETTINGS = SCHEMA_DIR / 'opensearch_settings.json'
OPENSEARCH_MAPPINGS = SCHEMA_DIR / 'opensearch_mappings.json'
MOCK_DATA = API_DIR / 'mock' / 'data.xlsx'

