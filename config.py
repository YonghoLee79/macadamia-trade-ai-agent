import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///macadamia_trade.db')
    
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
