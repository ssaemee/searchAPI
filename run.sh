#!/bin/bash

# 스크립트 위치 기준으로 루트 디렉토리로 이동
cd "$(dirname "$0")"

# 가상환경 활성화
source venv/bin/activate

# FastAPI 서버 실행
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

