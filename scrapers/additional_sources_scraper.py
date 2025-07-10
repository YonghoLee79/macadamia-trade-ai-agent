import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import logging
import os
import random
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdditionalSourcesScraper:
    """추가 데이터 소스 스크래퍼 (KITA, FAOSTAT, World Bank 등)"""
    
    def __init__(self, session):
        self.session = session
        self.is_railway = os.getenv('RAILWAY_ENVIRONMENT') is not None
        
    def scrape_additional_real_sources(self) -> List[Dict]:
        """추가 실제 데이터 소스들에서 무역 데이터 수집"""
        all_trade_data = []
        
        # 각 소스별로 데이터 수집
        sources = [
            self._scrape_kita_data,
            self._scrape_faostat_data, 
            self._scrape_worldbank_data,
            self._scrape_trading_economics_data,
            self._scrape_usda_data,
            self._scrape_eurostat_data
        ]
        
        for scraper_func in sources:
            try:
                data = scraper_func()
                all_trade_data.extend(data)
                time.sleep(2)  # 소스간 간격
            except Exception as e:
                logger.error(f"{scraper_func.__name__} 데이터 수집 오류: {e}")
                continue
                
        logger.info(f"추가 소스에서 총 {len(all_trade_data)}건 수집")
        return all_trade_data
    
    def _scrape_kita_data(self) -> List[Dict]:
        """KITA (한국무역협회) 데이터 수집"""
        trade_data = []
        
        try:
            logger.info("KITA 무역통계 수집 시도...")
            
            # KITA 무역통계 서비스
            urls = [
                "https://stat.kita.net/stat/kts/ctr/CtrTotalImpExpList.screen",
                "https://www.kita.net/cmmrcInfo/cmmrcNews/cmercNews/cmercNewsDetail.do"
            ]
            
            for url in urls:
                try:
                    response = self.session.get(url, timeout=30)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # KITA 통계 테이블 찾기
                        tables = soup.find_all('table', class_='table')
                        for table in tables:
                            rows = table.find_all('tr')
                            for row in rows[1:]:  # 헤더 제외
                                cells = row.find_all(['td', 'th'])
                                if len(cells) >= 4:
                                    trade_data.append({
                                        'country_origin': cells[0].get_text(strip=True),
                                        'country_destination': 'Korea',
                                        'product_code': '080250',
                                        'product_description': '견과류(마카다미아)',
                                        'trade_value': self._parse_number(cells[2].get_text(strip=True)),
                                        'quantity': self._parse_number(cells[3].get_text(strip=True)),
                                        'trade_type': 'import',
                                        'period': datetime.now().strftime('%Y%m'),
                                        'year': datetime.now().year,
                                        'source': 'KITA'
                                    })
                        
                        if trade_data:
                            break
                            
                except Exception as e:
                    logger.error(f"KITA URL {url} 오류: {e}")
                    
        except Exception as e:
            logger.error(f"KITA 데이터 수집 오류: {e}")
            
        logger.info(f"KITA에서 {len(trade_data)}건 수집")
        return trade_data
    
    def _scrape_faostat_data(self) -> List[Dict]:
        """FAOSTAT 농업 무역 데이터 수집"""
        trade_data = []
        
        try:
            logger.info("FAOSTAT 농업 무역 데이터 수집 시도...")
            
            # FAOSTAT API
            url = "https://fenixservices.fao.org/faostat/api/v1/en/data/TM"
            
            params = {
                'area': '136',  # 한국
                'element': '5622,5922',  # 수입량, 수입액
                'item': '256',  # 견과류
                'year': '2020:2024',
                'format': 'json'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    for record in data['data']:
                        trade_data.append({
                            'country_origin': record.get('ReporterCountry', ''),
                            'country_destination': 'Korea',
                            'product_code': record.get('ItemCode', ''),
                            'product_description': record.get('Item', '견과류'),
                            'trade_value': record.get('Value', 0),
                            'quantity': 0,  # FAOSTAT에서는 별도 필드
                            'trade_type': 'import',
                            'period': record.get('Year', ''),
                            'year': int(record.get('Year', datetime.now().year)),
                            'source': 'FAOSTAT'
                        })
                    
                    logger.info(f"FAOSTAT에서 {len(trade_data)}건 수집")
            else:
                logger.warning(f"FAOSTAT API 호출 실패: {response.status_code}")
                
        except Exception as e:
            logger.error(f"FAOSTAT 데이터 수집 오류: {e}")
            
        return trade_data
    
    def _scrape_worldbank_data(self) -> List[Dict]:
        """World Bank 무역 데이터 수집"""
        trade_data = []
        
        try:
            logger.info("World Bank 무역 데이터 수집 시도...")
            
            # World Bank API
            url = "https://api.worldbank.org/v2/country/KOR/indicator/TM.VAL.AGRI.ZS.UN"
            
            params = {
                'format': 'json',
                'date': '2020:2024',
                'per_page': 1000
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1 and isinstance(data[1], list):
                    for record in data[1]:
                        if record.get('value'):
                            trade_data.append({
                                'country_origin': 'Global',
                                'country_destination': 'Korea',
                                'product_code': 'AGRI',
                                'product_description': '농산물(견과류 포함)',
                                'trade_value': record.get('value', 0),
                                'quantity': 0,
                                'trade_type': 'import',
                                'period': record.get('date', ''),
                                'year': int(record.get('date', datetime.now().year)),
                                'source': 'World_Bank'
                            })
                    
                    logger.info(f"World Bank에서 {len(trade_data)}건 수집")
            else:
                logger.warning(f"World Bank API 호출 실패: {response.status_code}")
                
        except Exception as e:
            logger.error(f"World Bank 데이터 수집 오류: {e}")
            
        return trade_data
    
    def _scrape_trading_economics_data(self) -> List[Dict]:
        """Trading Economics 데이터 수집"""
        trade_data = []
        
        try:
            logger.info("Trading Economics 데이터 수집 시도...")
            
            # Trading Economics 공개 페이지
            url = "https://tradingeconomics.com/south-korea/imports"
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 수입 통계 테이블 찾기
                tables = soup.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    for row in rows[1:]:
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 3:
                            trade_data.append({
                                'country_origin': 'Global',
                                'country_destination': 'Korea',
                                'product_code': 'TOTAL',
                                'product_description': '전체 수입',
                                'trade_value': self._parse_number(cells[1].get_text(strip=True)),
                                'quantity': 0,
                                'trade_type': 'import',
                                'period': cells[0].get_text(strip=True),
                                'year': datetime.now().year,
                                'source': 'Trading_Economics'
                            })
                
                logger.info(f"Trading Economics에서 {len(trade_data)}건 수집")
                
        except Exception as e:
            logger.error(f"Trading Economics 데이터 수집 오류: {e}")
            
        return trade_data
    
    def _scrape_usda_data(self) -> List[Dict]:
        """USDA 농업 무역 데이터 수집"""
        trade_data = []
        
        try:
            logger.info("USDA 농업 무역 데이터 수집 시도...")
            
            # USDA FAS 데이터
            url = "https://apps.fas.usda.gov/psdonline/api/psd/commodity"
            
            params = {
                'commodity_code': '8',  # Tree nuts
                'country_code': '136',  # South Korea
                'format': 'json'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    for record in data:
                        trade_data.append({
                            'country_origin': 'USA',
                            'country_destination': 'Korea',
                            'product_code': '8',
                            'product_description': '견과류',
                            'trade_value': record.get('Value', 0),
                            'quantity': 0,
                            'trade_type': 'import',
                            'period': record.get('Market_Year', ''),
                            'year': datetime.now().year,
                            'source': 'USDA'
                        })
                
                logger.info(f"USDA에서 {len(trade_data)}건 수집")
                
        except Exception as e:
            logger.error(f"USDA 데이터 수집 오류: {e}")
            
        return trade_data
    
    def _scrape_eurostat_data(self) -> List[Dict]:
        """Eurostat 무역 데이터 수집"""
        trade_data = []
        
        try:
            logger.info("Eurostat 무역 데이터 수집 시도...")
            
            # Eurostat API
            url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ext_lt_maineu"
            
            params = {
                'format': 'JSON',
                'geo': 'KR',  # Korea
                'sitc06': 'TOTAL',
                'time': '2020:2024'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'value' in data:
                    for key, value in data['value'].items():
                        trade_data.append({
                            'country_origin': 'EU',
                            'country_destination': 'Korea',
                            'product_code': 'TOTAL',
                            'product_description': '전체 무역',
                            'trade_value': value,
                            'quantity': 0,
                            'trade_type': 'import',
                            'period': key,
                            'year': datetime.now().year,
                            'source': 'Eurostat'
                        })
                
                logger.info(f"Eurostat에서 {len(trade_data)}건 수집")
                
        except Exception as e:
            logger.error(f"Eurostat 데이터 수집 오류: {e}")
            
        return trade_data
    
    def _parse_number(self, text: str) -> float:
        """텍스트에서 숫자 추출"""
        try:
            # 쉼표, 공백 제거 후 숫자 변환
            cleaned = text.replace(',', '').replace(' ', '').strip()
            return float(cleaned) if cleaned else 0.0
        except (ValueError, AttributeError):
            return 0.0
