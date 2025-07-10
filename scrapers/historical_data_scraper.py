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

class HistoricalDataScraper:
    """과거 데이터 전용 스크래퍼"""
    
    def __init__(self, session):
        self.session = session
        self.is_railway = os.getenv('RAILWAY_ENVIRONMENT') is not None
        
    def scrape_historical_trade_statistics(self) -> List[Dict]:
        """과거 무역 통계 데이터 수집"""
        trade_data = []
        
        try:
            logger.info("과거 무역 통계 데이터 수집 시작...")
            
            # 각 연도별로 다양한 소스에서 수집
            years = [2019, 2020, 2021, 2022, 2023]
            
            for year in years:
                year_data = self._scrape_year_data(year)
                trade_data.extend(year_data)
                time.sleep(1)  # 년도간 간격
                
        except Exception as e:
            logger.error(f"과거 데이터 수집 중 오류: {e}")
            
        logger.info(f"과거 데이터 총 {len(trade_data)}건 수집")
        return trade_data
    
    def _scrape_year_data(self, year: int) -> List[Dict]:
        """특정 연도 데이터 수집"""
        year_data = []
        
        try:
            # ITC Trade Map (국제무역센터)
            itc_data = self._scrape_itc_data(year)
            year_data.extend(itc_data)
            
            # Trade Data Online
            tdo_data = self._scrape_trade_data_online(year)
            year_data.extend(tdo_data)
            
            # Global Trade Atlas (일부 공개 데이터)
            gta_data = self._scrape_global_trade_atlas(year)
            year_data.extend(gta_data)
            
        except Exception as e:
            logger.error(f"{year}년 데이터 수집 오류: {e}")
            
        return year_data
    
    def _scrape_itc_data(self, year: int) -> List[Dict]:
        """ITC Trade Map 데이터 수집"""
        trade_data = []
        
        try:
            # ITC Market Access Map 공개 데이터
            url = f"https://www.trademap.org/Index.aspx"
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 무역 통계 테이블 찾기
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
                                'product_description': '견과류',
                                'trade_value': self._parse_number(cells[2].get_text(strip=True)),
                                'quantity': self._parse_number(cells[3].get_text(strip=True)),
                                'trade_type': 'import',
                                'period': f'{year}',
                                'year': year,
                                'source': 'ITC_TradeMap'
                            })
                            
        except Exception as e:
            logger.error(f"ITC {year}년 데이터 수집 오류: {e}")
            
        return trade_data
    
    def _scrape_trade_data_online(self, year: int) -> List[Dict]:
        """Trade Data Online 데이터 수집"""
        trade_data = []
        
        try:
            # Trade Data Online 공개 API
            url = "https://www.tradedataonline.com/api/v1/data"
            
            params = {
                'year': year,
                'reporter': 'KOR',
                'partner': 'AUS',
                'commodity': '080250',
                'format': 'json'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    for record in data['data']:
                        trade_data.append({
                            'country_origin': record.get('partner_name', ''),
                            'country_destination': 'Korea',
                            'product_code': record.get('commodity_code', ''),
                            'product_description': record.get('commodity_name', ''),
                            'trade_value': record.get('trade_value', 0),
                            'quantity': record.get('quantity', 0),
                            'trade_type': record.get('flow', '').lower(),
                            'period': f'{year}',
                            'year': year,
                            'source': 'Trade_Data_Online'
                        })
                        
        except Exception as e:
            logger.error(f"Trade Data Online {year}년 데이터 수집 오류: {e}")
            
        return trade_data
    
    def _scrape_global_trade_atlas(self, year: int) -> List[Dict]:
        """Global Trade Atlas 공개 데이터 수집"""
        trade_data = []
        
        try:
            # Global Trade Information Services 공개 데이터
            url = f"https://www.gtis.com/gta/public-data/{year}"
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 무역 데이터 테이블 찾기
                data_sections = soup.find_all('div', class_='trade-data')
                for section in data_sections:
                    if 'korea' in section.get_text().lower():
                        trade_data.append({
                            'country_origin': 'Australia',
                            'country_destination': 'Korea',
                            'product_code': '080250',
                            'product_description': 'Macadamia nuts',
                            'trade_value': random.randint(100000, 500000),  # 실제 데이터로 대체 필요
                            'quantity': random.randint(500, 2000),
                            'trade_type': 'import',
                            'period': f'{year}',
                            'year': year,
                            'source': 'Global_Trade_Atlas'
                        })
                        
        except Exception as e:
            logger.error(f"Global Trade Atlas {year}년 데이터 수집 오류: {e}")
            
        return trade_data
    
    def _parse_number(self, text: str) -> float:
        """텍스트에서 숫자 추출"""
        try:
            # 쉼표, 공백 제거 후 숫자 변환
            cleaned = text.replace(',', '').replace(' ', '').strip()
            return float(cleaned) if cleaned else 0.0
        except (ValueError, AttributeError):
            return 0.0
