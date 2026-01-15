#!/bin/bash

# 로그 정리 스크립트
# 사용법: ./clean_logs.sh [일수]
# 예: ./clean_logs.sh 7 (7일 이전 삭제), ./clean_logs.sh 0 (전체 삭제)

cd "$(dirname "$0")"

LOGS_DIR="logs"
DAYS=${1:-7}

echo "=== 로그 정리 ==="

if [ "$DAYS" -eq 0 ]; then
    echo "모든 로그 파일 삭제"
    rm -f "$LOGS_DIR"/*.log
else
    echo "${DAYS}일 이전 로그 삭제"
    find "$LOGS_DIR" -name "*.log" -mtime +$DAYS -delete
fi

echo "완료"
