"""
Flask 앱 설정 및 초기화
"""
from flask import Flask
from flask_cors import CORS
import os
import logging
import threading
from config import Config
from models import DatabaseManager
from data_scraper import MacadamiaTradeDataScraper
from ai_agent import MacadamiaTradeAIAgent
from scheduler import MacadamiaTradeScheduler

logger = logging.getLogger(__name__)

class FlaskAppConfig:
    """Flask 앱 설정 클래스"""
    
    def __init__(self):
        self.app = None
        self.config = Config()
        self.db_manager = None
        self.scraper = None
        self.ai_agent = None
        self.scheduler = None
        self.scheduler_thread = None
        
    def create_app(self):
        """Flask 앱 생성 및 설정"""
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'macadamia-trade-secret-key')
        
        # 로깅 설정
        logging.basicConfig(level=logging.INFO)
        
        # 컴포넌트 초기화
        self._initialize_components()
        
        # 스케줄러 시작
        self._start_scheduler()
        
        return self.app
    
    def _initialize_components(self):
        """주요 컴포넌트 초기화"""
        try:
            # 데이터베이스 매니저
            self.db_manager = DatabaseManager(self.config.DATABASE_URL)
            logger.info("Database Manager initialized")
            
            # 데이터 스크래퍼
            self.scraper = MacadamiaTradeDataScraper()
            logger.info("Data Scraper initialized")
            
            # AI Agent (선택적)
            try:
                self.ai_agent = MacadamiaTradeAIAgent()
                logger.info("AI Agent initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize AI Agent: {e}")
                self.ai_agent = None
            
            # 스케줄러
            self.scheduler = MacadamiaTradeScheduler()
            logger.info("Scheduler initialized")
            
        except Exception as e:
            logger.error(f"Component initialization error: {e}")
            raise
    
    def _start_scheduler(self):
        """백그라운드 스케줄러 시작"""
        def run_scheduler():
            try:
                self.scheduler.start_scheduler()
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
        
        # 백그라운드 스케줄러 시작
        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()
        logger.info("Background scheduler started")
    
    def get_components(self):
        """초기화된 컴포넌트들 반환"""
        return {
            'app': self.app,
            'config': self.config,
            'db_manager': self.db_manager,
            'scraper': self.scraper,
            'ai_agent': self.ai_agent,
            'scheduler': self.scheduler
        }

# 전역 함수들 추가
def create_app():
    """Flask 앱 생성 함수"""
    import os
    # 템플릿 폴더 경로를 명시적으로 지정
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    CORS(app)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'macadamia-trade-secret-key')
    
    # 로깅 설정
    logging.basicConfig(level=logging.INFO)
    
    logger.info(f"Template folder: {template_dir}")
    logger.info(f"Static folder: {static_dir}")
    
    return app

def create_components():
    """주요 컴포넌트 생성 함수"""
    try:
        config = Config()
        
        # 데이터베이스 매니저
        db_manager = DatabaseManager(config.DATABASE_URL)
        logger.info("Database Manager initialized")
        
        # 데이터 스크래퍼
        scraper = MacadamiaTradeDataScraper()
        logger.info("Data Scraper initialized")
        
        # AI Agent (선택적)
        try:
            ai_agent = MacadamiaTradeAIAgent()
            logger.info("AI Agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI Agent: {e}")
            ai_agent = None
        
        # 스케줄러
        scheduler = MacadamiaTradeScheduler()
        logger.info("Scheduler initialized")
        
        return {
            'config': config,
            'db_manager': db_manager,
            'scraper': scraper,
            'ai_agent': ai_agent,
            'scheduler': scheduler
        }
        
    except Exception as e:
        logger.error(f"Component initialization error: {e}")
        raise
