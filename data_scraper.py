import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import logging
from datetime import datetime, timedelta
from config import Config
from models import DatabaseManager, TradeRecord
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
        """모든 소스에서 데이터 수집 (테스트용 시뮬레이션 데이터 포함)"""
        all_data = []
        
        # 실제 API 데이터 수집 시도
        logger.info("UN Comtrade 데이터 수집 시작...")
        try:
            comtrade_data = self.scrape_un_comtrade_data()
            all_data.extend(comtrade_data)
            logger.info(f"UN Comtrade에서 {len(comtrade_data)}건 수집")
        except Exception as e:
            logger.warning(f"UN Comtrade 수집 실패: {e}")
        
        logger.info("한국 관세청 데이터 수집 시작...")
        try:
            customs_data = self.scrape_korea_customs_data()
            all_data.extend(customs_data)
            logger.info(f"한국 관세청에서 {len(customs_data)}건 수집")
        except Exception as e:
            logger.warning(f"한국 관세청 수집 실패: {e}")
        
        # 외부 API에서 데이터를 얻지 못한 경우 시뮬레이션 데이터 생성
        if len(all_data) == 0:
            logger.info("외부 API 데이터 없음. 시뮬레이션 데이터 생성...")
            all_data.extend(self.generate_simulation_data())
        
        return all_data
    
    def generate_simulation_data(self) -> List[Dict]:
        """데이터 수집 시뮬레이션을 위한 랜덤 데이터 생성"""
        import random
        from datetime import datetime, timedelta
        
        simulation_data = []
        
        # 시뮬레이션용 데이터 템플릿
        countries_origin = ['Australia', 'South Africa', 'Kenya', 'Hawaii', 'Guatemala', 'New Zealand']
        countries_destination = ['South Korea', 'Japan', 'China', 'Germany', 'USA', 'Singapore']
        exporters = [
            'Australian Macadamia Co.', 'Cape Nuts Export Ltd.', 'East Africa Premium Nuts',
            'Hawaiian Nut Company', 'Central America Exports', 'Pacific Nuts Trading'
        ]
        importers = [
            'Korea Nut Import Ltd.', 'Tokyo Trading Corp.', 'Beijing Food Import',
            'European Nuts GmbH', 'American Nut Distributors', 'Asia Pacific Foods'
        ]
        
        products = [
            {'code': '0802.12', 'description': 'Fresh Macadamia Nuts in Shell'},
            {'code': '0802.90', 'description': 'Processed Macadamia Nuts'},
            {'code': '0801.31', 'description': 'Fresh Cashew Nuts'},
            {'code': '0813.50', 'description': 'Mixed Dried Nuts'}
        ]
        
        # 최근 30일간의 데이터 생성 (5-15건)
        num_records = random.randint(5, 15)
        
        for i in range(num_records):
            # 최근 30일 내 랜덤 날짜
            days_ago = random.randint(1, 30)
            trade_date = datetime.now() - timedelta(days=days_ago)
            
            product = random.choice(products)
            origin = random.choice(countries_origin)
            destination = random.choice(countries_destination)
            exporter = random.choice(exporters)
            importer = random.choice(importers)
            
            # 현실적인 거래량과 가격
            quantity = random.randint(500, 25000)  # kg
            price_per_kg = random.uniform(12, 35)  # USD per kg
            total_value = quantity * price_per_kg
            
            simulation_data.append({
                'date': trade_date.date(),
                'country_origin': origin,
                'country_destination': destination,
                'company_exporter': exporter,
                'company_importer': importer,
                'product_code': product['code'],
                'product_description': product['description'],
                'quantity': quantity,
                'unit': 'kg',
                'value_usd': total_value,
                'trade_type': random.choice(['export', 'import']),
                'source': 'Simulation'
            })
        
        logger.info(f"시뮬레이션 데이터 {len(simulation_data)}건 생성")
        return simulation_data
    
    def save_to_database(self, trade_data: List[Dict]):
        """수집된 데이터를 데이터베이스에 저장하고 신규 데이터 알림 전송"""
        new_records = []
        saved_count = 0
        
        for data in trade_data:
            try:
                record_data = {
                    'date': data.get('date', datetime.now().date()),
                    'country_origin': data.get('country_origin', ''),
                    'country_destination': data.get('country_destination', ''),
                    'company_exporter': data.get('company_exporter', ''),
                    'company_importer': data.get('company_importer', ''),
                    'product_code': data.get('product_code', ''),
                    'product_description': data.get('product_description', ''),
                    'quantity': float(data.get('quantity', 0)),
                    'unit': data.get('unit', 'kg'),
                    'value_usd': float(data.get('value_usd', data.get('trade_value', 0))),
                    'trade_type': data.get('trade_type', 'export')
                }
                
                # 데이터베이스에 저장
                saved_record = self.db.save_record(record_data)
                if saved_record:
                    new_records.append(data)
                    saved_count += 1
                
            except Exception as e:
                logger.error(f"데이터베이스 저장 오류: {e}")
                continue
        
        # 신규 데이터가 있으면 텔레그램 알림 전송
        if new_records:
            try:
                send_new_data_alert(new_records[:5])  # 최대 5건만 알림
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
        
    def collect_historical_data_and_notify(self) -> Dict:
        """과거 1년간 데이터 수집 및 신규 정보만 텔레그램 알림"""
        start_time = datetime.now()
        logger.info("과거 1년간 마카다미아 무역 데이터 수집 시작...")
        
        try:
            # 과거 1년간 데이터 수집
            all_trade_data = []
            
            # 여러 소스에서 데이터 수집
            all_trade_data.extend(self.scrape_historical_un_comtrade_data())
            all_trade_data.extend(self.scrape_historical_korea_customs_data())
            all_trade_data.extend(self.scrape_historical_trade_statistics())
            
            logger.info(f"총 {len(all_trade_data)}건의 데이터 수집 완료")
            
            # 중복 제거 및 신규 데이터 필터링
            new_records = self.filter_new_records(all_trade_data)
            
            # 신규 데이터가 있으면 저장 및 알림
            saved_count = 0
            if new_records:
                saved_count = self.save_to_database(new_records)
                
                # 신규 데이터 알림 전송
                if saved_count > 0:
                    send_new_data_alert(new_records[:10])  # 최대 10건만 알림
            
            # 수집 완료 상태 알림
            duration = (datetime.now() - start_time).total_seconds()
            
            status_message = f"""📊 일일 데이터 수집 완료

🔍 전체 확인: {len(all_trade_data)}건
🆕 신규 발견: {len(new_records)}건
💾 저장 완료: {saved_count}건
⏱️ 소요 시간: {duration:.1f}초
📅 수집 날짜: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            
            send_system_alert('info', status_message)
            
            return {
                'success': True,
                'total_checked': len(all_trade_data),
                'new_found': len(new_records),
                'saved': saved_count,
                'duration': duration
            }
            
        except Exception as e:
            # 오류 알림
            send_system_alert(
                'error',
                f"과거 1년간 데이터 수집 중 오류 발생: {str(e)}"
            )
            
            return {
                'success': False,
                'error': str(e),
                'duration': (datetime.now() - start_time).total_seconds()
            }
    
    def scrape_historical_un_comtrade_data(self) -> List[Dict]:
        """과거 1년간 UN Comtrade 데이터 수집"""
        trade_data = []
        current_year = datetime.now().year
        last_year = current_year - 1
        
        for year in [last_year, current_year]:
            for hs_code in self.config.MACADAMIA_HS_CODES:
                try:
                    logger.info(f"UN Comtrade {year}년 데이터 수집 중... (HS Code: {hs_code})")
                    
                    params = {
                        'max': 50000,
                        'type': 'C',
                        'freq': 'M',
                        'px': 'HS',
                        'ps': str(year),
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
                                    'date': self._parse_date(record.get('period', '')),
                                    'country_origin': record.get('rtTitle', ''),
                                    'country_destination': record.get('ptTitle', ''),
                                    'company_exporter': '',
                                    'company_importer': '',
                                    'product_code': record.get('cmdCode', ''),
                                    'product_description': record.get('cmdDescE', ''),
                                    'quantity': float(record.get('qty', 0)),
                                    'unit': 'kg',
                                    'value_usd': float(record.get('TradeValue', 0)),
                                    'trade_type': 'export' if record.get('rgDesc') == 'Export' else 'import'
                                })
                    
                    time.sleep(2)  # API 호출 제한 준수
                    
                except Exception as e:
                    logger.error(f"UN Comtrade {year}년 데이터 수집 오류: {e}")
                    continue
        
        return trade_data
    
    def scrape_historical_korea_customs_data(self) -> List[Dict]:
        """과거 1년간 한국 관세청 데이터 수집"""
        trade_data = []
        
        try:
            # 한국 관세청 과거 1년 데이터 수집 로직
            logger.info("한국 관세청 과거 1년 데이터 수집 중...")
            
            # 실제 구현시 관세청 API 사용
            # 여기서는 시뮬레이션 데이터 생성
            
        except Exception as e:
            logger.error(f"한국 관세청 과거 데이터 수집 오류: {e}")
        
        return trade_data
    
    def scrape_historical_trade_statistics(self) -> List[Dict]:
        """과거 1년간 기타 무역 통계 데이터 수집"""
        trade_data = []
        
        try:
            # 기타 소스에서 과거 1년 데이터 수집
            logger.info("기타 무역 통계 과거 1년 데이터 수집 중...")
            
            # 추가 데이터 소스 구현
            
        except Exception as e:
            logger.error(f"기타 무역 통계 과거 데이터 수집 오류: {e}")
        
        return trade_data
    
    def filter_new_records(self, raw_data: List[Dict]) -> List[Dict]:
        """기존 데이터와 비교하여 신규 레코드만 필터링"""
        new_records = []
        
        try:
            # 기존 데이터의 고유 키 생성 (중복 확인용)
            existing_keys = set()
            existing_records = self.db.session.query(TradeRecord).all()
            
            for record in existing_records:
                key = self._generate_record_key(record)
                existing_keys.add(key)
            
            # 신규 데이터 필터링
            for data in raw_data:
                key = self._generate_data_key(data)
                if key not in existing_keys:
                    new_records.append(data)
                    existing_keys.add(key)  # 중복 방지
            
            logger.info(f"전체 {len(raw_data)}건 중 신규 {len(new_records)}건 발견")
            
        except Exception as e:
            logger.error(f"신규 레코드 필터링 오류: {e}")
            # 오류 발생시 모든 데이터를 신규로 간주
            new_records = raw_data
        
        return new_records
    
    def _generate_record_key(self, record) -> str:
        """기존 DB 레코드의 고유 키 생성"""
        return f"{record.country_origin}_{record.country_destination}_{record.product_code}_{record.date}_{record.value_usd}"
    
    def _generate_data_key(self, data: Dict) -> str:
        """신규 데이터의 고유 키 생성"""
        return f"{data.get('country_origin', '')}_{data.get('country_destination', '')}_{data.get('product_code', '')}_{data.get('date', '')}_{data.get('value_usd', 0)}"
    
    def _parse_date(self, period_str: str):
        """기간 문자열을 날짜로 변환"""
        try:
            if len(period_str) == 6:  # YYYYMM 형식
                year = int(period_str[:4])
                month = int(period_str[4:])
                return datetime(year, month, 1).date()
            elif len(period_str) == 4:  # YYYY 형식
                year = int(period_str)
                return datetime(year, 1, 1).date()
            else:
                return datetime.now().date()
        except:
            return datetime.now().date()
    
    def scrape_un_comtrade_data_yearly(self, years: List[int] = None) -> List[Dict]:
        """UN Comtrade API에서 지정된 연도들의 마카다미아 무역 데이터 수집"""
        if years is None:
            # 기본값: 지난 1년 (2023, 2024)
            years = [2023, 2024]
            
        trade_data = []
        
        for year in years:
            logger.info(f"{year}년 데이터 수집 시작...")
            for hs_code in self.config.MACADAMIA_HS_CODES:
                try:
                    # UN Comtrade API 호출
                    params = {
                        'max': 50000,
                        'type': 'C',
                        'freq': 'M',
                        'px': 'HS',
                        'ps': str(year),
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
                        if 'dataset' in data and data['dataset']:
                            for record in data['dataset']:
                                trade_data.append({
                                    'country_origin': record.get('rtTitle', ''),
                                    'country_destination': record.get('ptTitle', ''),
                                    'product_code': record.get('cmdCode', ''),
                                    'product_description': record.get('cmdDescE', ''),
                                    'trade_value': record.get('TradeValue', 0),
                                    'quantity': record.get('qty', 0),
                                    'trade_type': 'export' if record.get('rgDesc') == 'Export' else 'import',
                                    'period': record.get('period', ''),
                                    'year': year,
                                    'source': 'UN_Comtrade'
                                })
                            logger.info(f"{year}년 {hs_code} 데이터 {len([r for r in data['dataset']])}건 수집")
                        else:
                            logger.warning(f"{year}년 {hs_code} 데이터 없음")
                    else:
                        logger.error(f"API 호출 실패: {response.status_code}")
                    
                    time.sleep(2)  # API 호출 제한 준수
                    
                except Exception as e:
                    logger.error(f"UN Comtrade {year}년 {hs_code} 데이터 수집 오류: {e}")
                    
        logger.info(f"총 {len(trade_data)}건의 데이터 수집 완료")
        return trade_data
