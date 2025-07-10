#!/usr/bin/env python3
"""
Railway 배포용 시작 스크립트
"""
import os
import sys
import logging
from app import app

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Railway 환경변수 확인
    logger.info("=== Railway Deployment Start ===")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Environment variables:")
    logger.info(f"  FLASK_ENV: {os.getenv('FLASK_ENV', 'not set')}")
    logger.info(f"  PORT: {os.getenv('PORT', 'not set')}")
    logger.info(f"  DATABASE_URL: {'set' if os.getenv('DATABASE_URL') else 'not set'}")
    
    # 포트 설정 (Railway 방식)
    port = 5000  # 기본값
    port_env = os.getenv('PORT')
    
    if port_env:
        try:
            port = int(port_env)
            logger.info(f"Using PORT from environment: {port}")
        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid PORT environment variable '{port_env}': {e}")
            logger.info(f"Using default port: {port}")
    else:
        logger.info(f"PORT not set, using default: {port}")
    
    # Flask 앱 시작
    logger.info(f"Starting Flask app on 0.0.0.0:{port}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
