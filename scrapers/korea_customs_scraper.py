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

class KoreaCustomsScraper:
    """한국 관세청 데이터 스크래퍼"""
    
    def __init__(self, session):
        self.session = session
        self.is_railway = os.getenv('RAILWAY_ENVIRONMENT') is not None
        
    def scrape_current_data(self) -> List[Dict]:
        """한국 관세청 데이터 수집 (실제 데이터)"""
        trade_data = []
        
        try:
            logger.info("한국 관세청 공개 API 호출 시도...")
            
            # 관세청 수출입무역통계 API 시도
            apis_to_try = [
                "https://unipass.customs.go.kr:38010/ext/rest/expDclrNtceQry/expDclrNtceQry",
                "https://www.customs.go.kr/kcs/na/ntt/selectNttList.do",
                "https://unipass.customs.go.kr:38010/ext/rest/expImpDclrQry/expImpDclrQry"
            ]
            
            for api_url in apis_to_try:
                try:
                    logger.info(f"API 시도: {api_url}")
                    
                    # 마카다미아 관련 파라미터
                    params = {
                        'hsSgn': '080250',  # 마카다미아 HS 코드
                        'expDclYy': '2024',
                        'stYm': '202401',
                        'edYm': '202412',
                        'cntyCd': '036',  # 호주
                        'format': 'json'
                    }
                    
                    response = self.session.get(api_url, params=params, timeout=30)
                    
                    if response.status_code == 200:
                        # 다양한 형태의 응답 처리
                        content_type = response.headers.get('content-type', '').lower()
                        
                        if 'json' in content_type:
                            try:
                                data = response.json()
                                if isinstance(data, dict) and ('expDclrNtceQryRtnVo' in data or 'data' in data):
                                    # 관세청 API 응답 구조에 맞게 파싱
                                    items = data.get('expDclrNtceQryRtnVo', {}).get('ntceQryRsltList', [])
                                    if not items:
                                        items = data.get('data', [])
                                    
                                    for item in items:
                                        trade_data.append({
                                            'country_origin': item.get('expCntyCd', ''),
                                            'country_destination': 'Korea',
                                            'product_code': item.get('hsSgn', ''),
                                            'product_description': item.get('prdlstNm', '마카다미아'),
                                            'trade_value': item.get('expUsdAmt', 0),
                                            'quantity': item.get('expKg', 0),
                                            'trade_type': 'import',
                                            'period': item.get('expDclYy', ''),
                                            'year': int(item.get('expDclYy', datetime.now().year)),
                                            'source': 'Korea_Customs'
                                        })
                                    
                                    if trade_data:
                                        logger.info(f"관세청에서 {len(trade_data)}건 데이터 수집")
                                        break
                                else:
                                    logger.warning("관세청 API 응답에 예상 데이터 없음")
                            except ValueError as e:
                                logger.error(f"관세청 JSON 파싱 오류: {e}")
                        else:
                            # HTML 응답인 경우 웹 스크래핑 시도
                            soup = BeautifulSoup(response.content, 'html.parser')
                            
                            # 관세청 웹사이트에서 무역통계 테이블 찾기
                            tables = soup.find_all('table')
                            for table in tables:
                                rows = table.find_all('tr')
                                for row in rows[1:]:  # 헤더 제외
                                    cells = row.find_all(['td', 'th'])
                                    if len(cells) >= 5:
                                        trade_data.append({
                                            'country_origin': cells[0].get_text(strip=True),
                                            'country_destination': 'Korea',
                                            'product_code': '080250',
                                            'product_description': '마카다미아',
                                            'trade_value': self._parse_number(cells[2].get_text(strip=True)),
                                            'quantity': self._parse_number(cells[3].get_text(strip=True)),
                                            'trade_type': 'import',
                                            'period': datetime.now().strftime('%Y%m'),
                                            'year': datetime.now().year,
                                            'source': 'Korea_Customs'
                                        })
                            
                            if trade_data:
                                logger.info(f"관세청 웹사이트에서 {len(trade_data)}건 데이터 수집")
                                break
                    else:
                        logger.warning(f"관세청 API 호출 실패: {response.status_code}")
                    
                    time.sleep(1)  # API 호출 제한 준수
                    
                except Exception as e:
                    logger.error(f"관세청 API {api_url} 호출 오류: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"관세청 데이터 수집 중 오류: {e}")
            
        logger.info(f"관세청에서 총 {len(trade_data)}건 수집")
        return trade_data
    
    def scrape_historical_data(self) -> List[Dict]:
        """한국 관세청 과거 데이터 수집"""
        trade_data = []
        
        try:
            logger.info("한국 관세청 과거 데이터 수집 시작...")
            
            # 2020-2023년 데이터 수집
            years = [2020, 2021, 2022, 2023]
            
            for year in years:
                try:
                    # 연도별 관세청 데이터 API 호출
                    url = "https://unipass.customs.go.kr:38010/ext/rest/expImpDclrQry/expImpDclrQry"
                    
                    params = {
                        'hsSgn': '080250',
                        'expDclYy': str(year),
                        'stYm': f'{year}01',
                        'edYm': f'{year}12',
                        'cntyCd': '036',
                        'format': 'json'
                    }
                    
                    response = self.session.get(url, params=params, timeout=30)
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            items = data.get('expDclrNtceQryRtnVo', {}).get('ntceQryRsltList', [])
                            
                            for item in items:
                                trade_data.append({
                                    'country_origin': item.get('expCntyCd', ''),
                                    'country_destination': 'Korea',
                                    'product_code': item.get('hsSgn', ''),
                                    'product_description': item.get('prdlstNm', '마카다미아'),
                                    'trade_value': item.get('expUsdAmt', 0),
                                    'quantity': item.get('expKg', 0),
                                    'trade_type': 'import',
                                    'period': f'{year}',
                                    'year': year,
                                    'source': 'Korea_Customs'
                                })
                            
                            logger.info(f"{year}년 관세청 데이터 {len(items)}건 수집")
                            
                        except ValueError as e:
                            logger.error(f"{year}년 관세청 JSON 파싱 오류: {e}")
                    else:
                        logger.warning(f"{year}년 관세청 API 호출 실패: {response.status_code}")
                    
                    time.sleep(2)  # API 호출 제한 준수
                    
                except Exception as e:
                    logger.error(f"{year}년 관세청 데이터 수집 오류: {e}")
                    
        except Exception as e:
            logger.error(f"관세청 과거 데이터 수집 중 오류: {e}")
            
        logger.info(f"관세청 과거 데이터 총 {len(trade_data)}건 수집")
        return trade_data
    
    def _parse_number(self, text: str) -> float:
        """텍스트에서 숫자 추출"""
        try:
            # 쉼표, 공백 제거 후 숫자 변환
            cleaned = text.replace(',', '').replace(' ', '').strip()
            return float(cleaned) if cleaned else 0.0
        except (ValueError, AttributeError):
            return 0.0
