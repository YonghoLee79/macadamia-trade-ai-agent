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
        return render_template('index.html')
    
    def health_check(self):
        """Railway 헬스체크용 엔드포인트"""
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }, 200
