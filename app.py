"""
마카다미아 무역 AI 에이전트 - 메인 Flask 애플리케이션
모듈화된 구조로 재작성됨
"""
import os
import logging
import threading
from flask import request

# 모듈화된 웹 컴포넌트들 import
from web import (
    create_app, create_components,
    DataAPIHandler, AIAPIHandler, ProductAPIHandler, ReportAPIHandler,
    DashboardAPI, TelegramAPI, DatabaseAPI, HealthAPI
)
from scheduler import MacadamiaTradeScheduler

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_modular_app():
    """모듈화된 Flask 애플리케이션 생성"""
    logger.info("Starting application initialization...")
    
    # Flask 앱과 공통 컴포넌트 생성
    app = create_app()
    logger.info("Flask app created successfully")
    
    components = create_components()
    logger.info("Components created successfully")
    
    # API 핸들러 인스턴스 생성
    data_api = DataAPIHandler(components)
    ai_api = AIAPIHandler(components)
    product_api = ProductAPIHandler(components)
    report_api = ReportAPIHandler(components)
    dashboard_api = DashboardAPI(components['db_manager'])
    telegram_api = TelegramAPI(components['db_manager'])
    database_api = DatabaseAPI(components['db_manager'], components['config'])
    health_api = HealthAPI()
    logger.info("API handlers created successfully")
    
    # 스케줄러 설정
    scheduler = MacadamiaTradeScheduler()
    logger.info("Scheduler initialized")
    
    # === 기본 라우트 ===
    @app.route('/')
    def index():
        return health_api.index()
    
    @app.route('/health')
    def health_check():
        return health_api.health_check()
    
    # === 대시보드 API ===
    @app.route('/api/dashboard')
    def dashboard_data():
        return dashboard_api.get_dashboard_data()
    
    @app.route('/api/status')
    def get_status():
        return dashboard_api.get_status()
    
    # === 데이터 수집 API ===
    @app.route('/api/data/latest')
    def get_latest_data():
        return data_api.get_latest_data()
    
    @app.route('/api/collect', methods=['POST'])
    def manual_collect():
        return data_api.manual_collect()
    
    @app.route('/api/data/statistics')
    def get_data_statistics():
        return data_api.get_data_statistics()
    
    @app.route('/api/data/historical/<int:days>')
    def get_historical_data(days):
        return data_api.get_historical_data(days)
    
    # === AI 분석 API ===
    @app.route('/api/analysis/<int:days>')
    def get_analysis(days):
        return ai_api.get_analysis(days)
    
    @app.route('/api/ai/insights', methods=['POST'])
    def get_ai_insights():
        return ai_api.get_ai_insights()
    
    @app.route('/api/ai/predictions', methods=['POST'])
    def get_ai_predictions():
        return ai_api.get_ai_predictions()
    
    # === 제품 검색 API ===
    @app.route('/api/products/search')
    def search_products():
        return product_api.search_products()
    
    @app.route('/api/products/categories')
    def get_product_categories():
        return product_api.get_product_categories()
    
    @app.route('/api/hscode/<hs_code>')
    def get_hscode_info(hs_code):
        return product_api.get_hscode_info(hs_code)
    
    # === 보고서 API ===
    @app.route('/api/reports')
    def get_reports():
        return report_api.get_reports()
    
    @app.route('/api/report/<filename>')
    def get_report_content(filename):
        return report_api.get_report_content(filename)
    
    @app.route('/api/generate-report', methods=['POST'])
    def generate_report():
        return report_api.generate_report()
    
    @app.route('/api/generate-sample-report', methods=['POST'])
    def generate_sample_report():
        return report_api.generate_sample_report()
    
    # === 텔레그램 API ===
    @app.route('/api/telegram/test', methods=['POST'])
    def test_telegram():
        return telegram_api.test_telegram()
    
    @app.route('/api/telegram/summary', methods=['POST'])
    def send_manual_summary():
        return telegram_api.send_manual_summary()
    
    # === 데이터베이스 API ===
    @app.route('/api/init-database', methods=['POST'])
    def init_database():
        return database_api.init_database()
    
    @app.route('/api/database/status')
    def database_status():
        return database_api.get_database_status()
    
    @app.route('/api/products/bulk-data', methods=['POST'])
    def upload_bulk_data():
        return database_api.upload_bulk_data(components['scraper'])
    
    # 스케줄러를 백그라운드에서 실행
    def run_scheduler():
        scheduler.start_scheduler()
    
    # 백그라운드 스케줄러 시작 (프로덕션 환경에서만)
    if os.getenv('FLASK_ENV') != 'development':
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        logger.info("Scheduler started in background")
    
    return app

# 애플리케이션 인스턴스 생성
try:
    # Railway 환경 변수 확인
    railway_env = os.getenv('RAILWAY_ENVIRONMENT')
    if railway_env:
        logger.info(f"Running in Railway environment: {railway_env}")
    
    app = create_modular_app()
    logger.info("Application created successfully")
except Exception as e:
    logger.error(f"Failed to create application: {e}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    # 최소한의 Flask 앱 생성
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def error_index():
        return f'''
        <html>
            <head><title>Application Error</title></head>
            <body>
                <h1>🚨 Application Start Error</h1>
                <p>Error: {str(e)}</p>
                <p><a href="/health">Health Check</a></p>
            </body>
        </html>
        ''', 500
    
    @app.route('/health')
    def error_health():
        return {'status': 'error', 'message': f'Application failed to start: {str(e)}'}, 500

if __name__ == '__main__':
    # Railway 포트 설정 처리
    try:
        port = int(os.getenv('PORT', '5000'))
    except (ValueError, TypeError):
        port = 5000
        logger.warning(f"Invalid PORT value: {os.getenv('PORT')}, using default 5000")
    
    logger.info(f"Starting modular Flask app on port {port}")
    app.run(
        debug=os.getenv('FLASK_ENV') == 'development', 
        host='0.0.0.0', 
        port=port
    )
