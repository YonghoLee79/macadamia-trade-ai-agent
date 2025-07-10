"""
헬스체크 및 기본 API 핸들러
"""
from flask import jsonify, render_template
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class HealthAPI:
    """헬스체크 및 기본 API 핸들러"""
    
    def __init__(self):
        pass
    
    def index(self):
        """메인 페이지"""
        try:
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Template rendering failed: {e}")
            return f'''
            <html>
                <head><title>마카다미아 무역 AI 에이전트</title></head>
                <body>
                    <h1>🌰 마카다미아 무역 AI 에이전트</h1>
                    <p>모듈화된 애플리케이션이 성공적으로 실행 중입니다!</p>
                    <p><a href="/health">헬스체크</a> | <a href="/api/dashboard">대시보드 API</a></p>
                    <p>Template 오류: {str(e)}</p>
                </body>
            </html>
            '''
    
    def health_check(self):
        """Railway 헬스체크용 엔드포인트"""
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }, 200
