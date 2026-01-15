#!/bin/bash

# 포트 8000에서 실행 중인 프로세스 종료
PORT=8000

echo "포트 $PORT 프로세스 확인 중..."

# 포트 사용 중인 PID 찾기
PIDS=$(lsof -ti:$PORT 2>/dev/null)

if [ -z "$PIDS" ]; then
    echo "포트 $PORT에서 실행 중인 프로세스가 없습니다."
else
    echo "종료할 프로세스: $PIDS"
    echo "$PIDS" | xargs kill -9 2>/dev/null
    echo "포트 $PORT 프로세스 종료 완료"
fi
