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

class UNComtradeScraper:
    """UN Comtrade API 데이터 스크래퍼"""
    
    def __init__(self, session):
        self.session = session
        self.is_railway = os.getenv('RAILWAY_ENVIRONMENT') is not None
        
    def scrape_current_data(self) -> List[Dict]:
        """UN Comtrade API에서 마카다미아 무역 데이터 수집 (실제 데이터)"""
        trade_data = []
        
        try:
            # 새로운 UN Comtrade API (comtradeapi.un.org) 사용
            logger.info("UN Comtrade 공개 API 호출 시도...")
            
            # 실제 API 엔드포인트 (공개 데이터)
            base_url = "https://comtradeapi.un.org/data/v1/get/C/A/HS"
            
            for hs_code in ['080250', '080290']:  # 마카다미아 HS 코드
                try:
                    # 실제 API 파라미터 구성
                    url = f"{base_url}/2023,2024/410/036/{hs_code}"  # 2023-2024년, 한국에서 호주로부터 수입
                    
                    # 요청 파라미터 추가
                    params = {
                        'format': 'json',
                        'aggregateBy': 'year',
                        'breakdownMode': 'classic',
                        'includeDesc': 'true'
                    }
                    
                    logger.info(f"UN Comtrade API 요청: {url}")
                    response = self.session.get(url, params=params, timeout=30)
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if 'data' in data and data['data']:
                                records = data['data']
                                logger.info(f"UN Comtrade에서 {len(records)}건 데이터 수신")
                                
                                for record in records:
                                    trade_data.append({
                                        'country_origin': record.get('reporterDesc', ''),
                                        'country_destination': record.get('partnerDesc', ''),
                                        'product_code': record.get('cmdCode', ''),
                                        'product_description': record.get('cmdDesc', ''),
                                        'trade_value': record.get('primaryValue', 0),
                                        'quantity': record.get('qty', 0),
                                        'trade_type': 'import' if record.get('flowDesc', '').lower() == 'imports' else 'export',
                                        'period': record.get('period', ''),
                                        'year': record.get('refYear', datetime.now().year),
                                        'source': 'UN_Comtrade'
                                    })
                            else:
                                logger.warning(f"UN Comtrade API에서 {hs_code} 데이터 없음")
                        except ValueError as e:
                            logger.error(f"UN Comtrade JSON 파싱 오류: {e}")
                            logger.error(f"응답 내용: {response.text[:500]}")
                    else:
                        logger.warning(f"UN Comtrade API 호출 실패: {response.status_code}")
                        logger.warning(f"응답: {response.text[:200]}")
                    
                    time.sleep(2)  # API 호출 제한 준수
                    
                except Exception as e:
                    logger.error(f"UN Comtrade {hs_code} 데이터 수집 오류: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"UN Comtrade 데이터 수집 중 오류: {e}")
            
        logger.info(f"UN Comtrade에서 총 {len(trade_data)}건 수집")
        return trade_data
    
    def scrape_historical_data(self) -> List[Dict]:
        """UN Comtrade 과거 데이터 수집"""
        trade_data = []
        
        try:
            logger.info("UN Comtrade 과거 데이터 수집 시작...")
            
            # 2020-2023년 데이터 수집
            years = [2020, 2021, 2022, 2023]
            base_url = "https://comtradeapi.un.org/data/v1/get/C/A/HS"
            
            for year in years:
                for hs_code in ['080250', '080290']:
                    try:
                        url = f"{base_url}/{year}/410/036/{hs_code}"
                        
                        response = self.session.get(url, timeout=30)
                        
                        if response.status_code == 200:
                            data = response.json()
                            if 'data' in data and data['data']:
                                for record in data['data']:
                                    trade_data.append({
                                        'country_origin': record.get('reporterDesc', ''),
                                        'country_destination': record.get('partnerDesc', ''),
                                        'product_code': record.get('cmdCode', ''),
                                        'product_description': record.get('cmdDesc', ''),
                                        'trade_value': record.get('primaryValue', 0),
                                        'quantity': record.get('qty', 0),
                                        'trade_type': 'import' if record.get('flowDesc', '').lower() == 'imports' else 'export',
                                        'period': record.get('period', ''),
                                        'year': year,
                                        'source': 'UN_Comtrade'
                                    })
                                logger.info(f"{year}년 {hs_code} 데이터 {len(data['data'])}건 수집")
                            else:
                                logger.warning(f"{year}년 {hs_code} 데이터 없음")
                        else:
                            logger.error(f"API 호출 실패: {response.status_code}")
                        
                        time.sleep(2)  # API 호출 제한 준수
                        
                    except Exception as e:
                        logger.error(f"UN Comtrade {year}년 {hs_code} 데이터 수집 오류: {e}")
                        
        except Exception as e:
            logger.error(f"UN Comtrade 과거 데이터 수집 중 오류: {e}")
            
        logger.info(f"UN Comtrade 과거 데이터 총 {len(trade_data)}건 수집")
        return trade_data
    
    def scrape_yearly_data(self, years: List[int] = None) -> List[Dict]:
        """특정 연도별 UN Comtrade 데이터 수집"""
        if not years:
            years = [2021, 2022, 2023, 2024]
            
        trade_data = []
        
        try:
            logger.info(f"UN Comtrade {years}년 데이터 수집 시작...")
            
            base_url = "https://comtradeapi.un.org/data/v1/get/C/A/HS"
            
            for year in years:
                for hs_code in ['080250', '080290']:
                    try:
                        url = f"{base_url}/{year}/410/036/{hs_code}"
                        
                        response = self.session.get(url, timeout=30)
                        
                        if response.status_code == 200:
                            data = response.json()
                            if 'data' in data and data['data']:
                                for record in data['data']:
                                    trade_data.append({
                                        'country_origin': record.get('reporterDesc', ''),
                                        'country_destination': record.get('partnerDesc', ''),
                                        'product_code': record.get('cmdCode', ''),
                                        'product_description': record.get('cmdDesc', ''),
                                        'trade_value': record.get('primaryValue', 0),
                                        'quantity': record.get('qty', 0),
                                        'trade_type': 'import' if record.get('flowDesc', '').lower() == 'imports' else 'export',
                                        'period': record.get('period', ''),
                                        'year': year,
                                        'source': 'UN_Comtrade'
                                    })
                                logger.info(f"{year}년 {hs_code} 데이터 {len(data['data'])}건 수집")
                            else:
                                logger.warning(f"{year}년 {hs_code} 데이터 없음")
                        else:
                            logger.error(f"API 호출 실패: {response.status_code}")
                        
                        time.sleep(2)  # API 호출 제한 준수
                        
                    except Exception as e:
                        logger.error(f"UN Comtrade {year}년 {hs_code} 데이터 수집 오류: {e}")
                        
        except Exception as e:
            logger.error(f"UN Comtrade 연도별 데이터 수집 중 오류: {e}")
            
        logger.info(f"UN Comtrade 연도별 데이터 총 {len(trade_data)}건 수집")
        return trade_data
