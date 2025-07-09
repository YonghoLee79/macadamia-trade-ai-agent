import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///macadamia_trade.db')
    
    # Telegram Settings
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    
    # 데이터 소스 URLs
    TRADE_DATA_SOURCES = {
        'comtrade': 'https://comtrade.un.org/api/get',
        'trademap': 'https://www.trademap.org',
        'customs_gov': 'https://unipass.customs.go.kr'
    }
    
    # 마카다미아 HS Code
    MACADAMIA_HS_CODES = [
        '080250',  # 마카다미아 너트 (껍질 있음)
        '080251',  # 마카다미아 너트 (껍질 없음)
    ]
    
    # 업데이트 스케줄
    UPDATE_SCHEDULE = "09:00"  # 매일 오전 9시
    
    # 공개 URL (ngrok 또는 배포된 서버 URL)
    PUBLIC_URL = os.getenv('PUBLIC_URL', 'http://localhost:5002')
    
    def get_dashboard_url(self):
        """대시보드 URL 반환 (공개 URL 우선)"""
        if self.PUBLIC_URL and not self.PUBLIC_URL.startswith('http://localhost'):
            return self.PUBLIC_URL
        else:
            return 'http://localhost:5002'
    
    def get_current_datetime(self):
        """현재 날짜시간 반환"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
