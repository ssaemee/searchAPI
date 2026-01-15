"""
로깅 설정
"""
import logging
from datetime import datetime
from pathlib import Path

# 로그 디렉토리 설정
ROOT_DIR = Path(__file__).parent.parent
LOGS_DIR = ROOT_DIR / 'logs'

# 로그 포맷
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y.%m.%d %H:%M:%S"


def ensure_logs_dir():
    """logs 디렉토리 생성"""
    LOGS_DIR.mkdir(exist_ok=True)


def get_log_filename() -> str:
    """날짜+시간 기반 로그 파일명 생성 (실행마다 새 파일)"""
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{now}.log"


def setup_logger(name: str = None, level: int = logging.INFO) -> logging.Logger:
    """
    로거 생성 및 설정
    
    :param name: 로거 이름 (None이면 root logger)
    :param level: 로깅 레벨
    :return: 설정된 로거
    """
    logger = logging.getLogger(name)
    
    # 이미 핸들러가 있으면 스킵
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    
    # 파일 핸들러 (날짜+시간별 로그 파일)
    ensure_logs_dir()
    log_file = LOGS_DIR / get_log_filename()
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    모듈용 로거 가져오기
    
    사용법:
        from core.logger import get_logger
        logger = get_logger(__name__)
        logger.info("메시지")
    """
    return setup_logger(name)
