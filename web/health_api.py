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
            logger.info("Attempting to render index.html template")
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Template rendering failed: {e}")
            # 더 나은 폴백 HTML 제공
            return f'''
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>마카다미아 무역 AI 에이전트</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body {{ background: linear-gradient(135deg, #ecf0f1 0%, #d5dbdb 100%); min-height: 100vh; }}
                    .container {{ margin-top: 50px; }}
                    .card {{ border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="row justify-content-center">
                        <div class="col-lg-8">
                            <div class="card">
                                <div class="card-header bg-success text-white text-center">
                                    <h1><i class="fas fa-seedling"></i> 마카다미아 무역 AI 에이전트</h1>
                                </div>
                                <div class="card-body text-center">
                                    <h3 class="text-success">🎉 모듈화된 애플리케이션이 성공적으로 실행 중입니다!</h3>
                                    <p class="lead">전 세계 마카다미아 무역 데이터를 실시간으로 분석하는 AI 에이전트입니다.</p>
                                    
                                    <div class="row mt-4">
                                        <div class="col-md-6 mb-3">
                                            <a href="/health" class="btn btn-outline-primary btn-lg w-100">
                                                <i class="fas fa-heartbeat"></i> 헬스체크
                                            </a>
                                        </div>
                                        <div class="col-md-6 mb-3">
                                            <a href="/api/dashboard" class="btn btn-outline-success btn-lg w-100">
                                                <i class="fas fa-chart-dashboard"></i> 대시보드 API
                                            </a>
                                        </div>
                                    </div>
                                    
                                    <div class="row">
                                        <div class="col-md-6 mb-3">
                                            <a href="/api/status" class="btn btn-outline-info btn-lg w-100">
                                                <i class="fas fa-info-circle"></i> 시스템 상태
                                            </a>
                                        </div>
                                        <div class="col-md-6 mb-3">
                                            <a href="/api/products/categories" class="btn btn-outline-warning btn-lg w-100">
                                                <i class="fas fa-tags"></i> 제품 카테고리
                                            </a>
                                        </div>
                                    </div>
                                    
                                    <hr class="my-4">
                                    <p class="text-muted">Template 경로 오류로 인해 기본 HTML을 표시 중입니다.</p>
                                    <small class="text-muted">오류: {str(e)}</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
                <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
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
