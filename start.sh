#!/bin/bash

# Railway 환경변수 디버깅
echo "=== Railway Environment Debug ==="
echo "PORT: ${PORT}"
echo "All environment variables:"
env | grep -E "(PORT|RAILWAY|DATABASE)" || echo "No relevant env vars found"
echo "================================="

# 포트 결정 (Railway에서 제공하는 PORT 또는 기본값 8080)
if [ -z "$PORT" ]; then
    echo "PORT not set, using 8080"
    export PORT=8080
else
    echo "Using PORT from environment: $PORT"
fi

# Gunicorn으로 Flask 앱 시작
echo "Starting Gunicorn on 0.0.0.0:$PORT"
exec gunicorn app:app --bind "0.0.0.0:$PORT" --workers 1 --timeout 120 --log-level info
