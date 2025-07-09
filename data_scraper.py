import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import logging
from datetime import datetime, timedelta
from config import Config
from models import DatabaseManager
from telegram_notifier import send_new_data_alert, send_system_alert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MacadamiaTradeDataScraper:
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager(self.config.DATABASE_URL)
        self.session = requests.Session()
        
    def scrape_un_comtrade_data(self) -> List[Dict]:
        """UN Comtrade API에서 마카다미아 무역 데이터 수집"""
        trade_data = []
        
        for hs_code in self.config.MACADAMIA_HS_CODES:
            try:
                # UN Comtrade API 호출
                params = {
                    'max': 50000,
                    'type': 'C',
                    'freq': 'M',
                    'px': 'HS',
                    'ps': '2024',
                    'r': 'all',
                    'p': 'all',
                    'rg': 'all',
                    'cc': hs_code,
                    'fmt': 'json'
                }
                
                response = self.session.get(
                    self.config.TRADE_DATA_SOURCES['comtrade'],
                    params=params,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if 'dataset' in data:
                        for record in data['dataset']:
                            trade_data.append({
                                'country_origin': record.get('rtTitle', ''),
                                'country_destination': record.get('ptTitle', ''),
                                'product_code': record.get('cmdCode', ''),
                                'product_description': record.get('cmdDescE', ''),
                                'trade_value': record.get('TradeValue', 0),
                                'quantity': record.get('qty', 0),
                                'trade_type': 'export' if record.get('rgDesc') == 'Export' else 'import',
                                'period': record.get('period', '')
                            })
                
                time.sleep(1)  # API 호출 제한 준수
                
            except Exception as e:
                logger.error(f"UN Comtrade 데이터 수집 오류: {e}")
                
        return trade_data
    
    def scrape_korea_customs_data(self) -> List[Dict]:
        """한국 관세청 데이터 수집"""
        trade_data = []
        
        try:
            # 관세청 API 또는 웹 스크래핑 구현
            # 실제 구현시에는 해당 API 키와 엔드포인트 사용
            logger.info("한국 관세청 데이터 수집 중...")
            
            # 예시 구조 (실제 API 엔드포인트로 교체 필요)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            # 여기서 실제 관세청 데이터 스크래핑 로직 구현
            
        except Exception as e:
            logger.error(f"한국 관세청 데이터 수집 오류: {e}")
            
        return trade_data
    
    def collect_all_data(self) -> List[Dict]:
        """모든 소스에서 데이터 수집"""
        all_data = []
        
        logger.info("UN Comtrade 데이터 수집 시작...")
        all_data.extend(self.scrape_un_comtrade_data())
        
        logger.info("한국 관세청 데이터 수집 시작...")
        all_data.extend(self.scrape_korea_customs_data())
        
        return all_data
    
    def save_to_database(self, trade_data: List[Dict]):
        """수집된 데이터를 데이터베이스에 저장하고 신규 데이터 알림 전송"""
        new_records = []
        saved_count = 0
        
        for data in trade_data:
            try:
                record_data = {
                    'date': pd.to_datetime('today').date(),
                    'country_origin': data.get('country_origin', ''),
                    'country_destination': data.get('country_destination', ''),
                    'company_exporter': data.get('company_exporter', ''),
                    'company_importer': data.get('company_importer', ''),
                    'product_code': data.get('product_code', ''),
                    'product_description': data.get('product_description', ''),
                    'quantity': float(data.get('quantity', 0)),
                    'value_usd': float(data.get('trade_value', 0)),
                    'trade_type': data.get('trade_type', '')
                }
                
                # 데이터베이스에 저장
                saved_record = self.db.add_record(record_data)
                if saved_record:
                    new_records.append(data)
                    saved_count += 1
                
            except Exception as e:
                logger.error(f"데이터베이스 저장 오류: {e}")
        
        # 신규 데이터가 있으면 텔레그램 알림 전송
        if new_records:
            try:
                send_new_data_alert(new_records)
                logger.info(f"텔레그램 신규 데이터 알림 전송: {len(new_records)}건")
            except Exception as e:
                logger.error(f"텔레그램 알림 전송 오류: {e}")
        
        return saved_count
    
    def collect_and_notify(self) -> Dict:
        """데이터 수집 및 결과 알림"""
        start_time = datetime.now()
        
        try:
            # 데이터 수집
            trade_data = self.collect_all_data()
            
            # 데이터베이스 저장
            saved_count = self.save_to_database(trade_data)
            
            # 수집 완료 알림
            duration = (datetime.now() - start_time).total_seconds()
            
            if saved_count > 0:
                send_system_alert(
                    'success',
                    f"데이터 수집 완료\n• 수집된 데이터: {len(trade_data)}건\n• 저장된 데이터: {saved_count}건\n• 소요 시간: {duration:.1f}초"
                )
            
            return {
                'success': True,
                'collected': len(trade_data),
                'saved': saved_count,
                'duration': duration
            }
            
        except Exception as e:
            # 오류 알림
            send_system_alert(
                'error',
                f"데이터 수집 중 오류 발생: {str(e)}"
            )
            
            return {
                'success': False,
                'error': str(e),
                'duration': (datetime.now() - start_time).total_seconds()
            }
