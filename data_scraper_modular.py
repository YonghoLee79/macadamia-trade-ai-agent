import requests
from typing import List, Dict
import time
import logging
import os
from datetime import datetime
from config import Config
from models import DatabaseManager, TradeRecord
from telegram_notifier import send_new_data_alert, send_system_alert
from trade_detail_generator import TradeDetailGenerator

# Import modular scrapers
from scrapers.un_comtrade_scraper import UNComtradeScraper
from scrapers.korea_customs_scraper import KoreaCustomsScraper
from scrapers.additional_sources_scraper import AdditionalSourcesScraper
from scrapers.public_data_scraper import PublicDataScraper
from scrapers.historical_data_scraper import HistoricalDataScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MacadamiaTradeDataScraper:
    """마카다미아 무역 데이터 수집 메인 클래스 (모듈화됨)"""
    
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager(self.config.DATABASE_URL)
        self.session = requests.Session()
        
        # Railway 환경 감지
        self.is_railway = os.getenv('RAILWAY_ENVIRONMENT') is not None
        if self.is_railway:
            logger.info("Railway 환경에서 실행 중")
        
        # 세션 설정
        self.session.headers.update({
            'User-Agent': 'MacadamiaTradeBot/1.0 (Railway Cloud Environment)' if self.is_railway else 'MacadamiaTradeBot/1.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        })
        
        # 모듈화된 스크래퍼들 초기화
        self.un_comtrade_scraper = UNComtradeScraper(self.session)
        self.korea_customs_scraper = KoreaCustomsScraper(self.session)
        self.additional_sources_scraper = AdditionalSourcesScraper(self.session)
        self.public_data_scraper = PublicDataScraper(self.session)
        self.historical_data_scraper = HistoricalDataScraper(self.session)
        
        # 상세 정보 생성기
        self.detail_generator = TradeDetailGenerator()
        
    def scrape_un_comtrade_data(self) -> List[Dict]:
        """UN Comtrade API에서 마카다미아 무역 데이터 수집 (실제 데이터)"""
        return self.un_comtrade_scraper.scrape_current_data()
    
    def scrape_korea_customs_data(self) -> List[Dict]:
        """한국 관세청 데이터 수집 (실제 데이터)"""
        return self.korea_customs_scraper.scrape_current_data()
    
    def scrape_additional_real_sources(self) -> List[Dict]:
        """추가 실제 데이터 소스들에서 무역 데이터 수집"""
        return self.additional_sources_scraper.scrape_additional_real_sources()
    
    def scrape_public_trade_data(self) -> List[Dict]:
        """다양한 공개 소스에서 실제 무역 데이터 수집"""
        return self.public_data_scraper.scrape_public_trade_data()
    
    def scrape_historical_un_comtrade_data(self) -> List[Dict]:
        """UN Comtrade 과거 데이터 수집"""
        return self.un_comtrade_scraper.scrape_historical_data()
    
    def scrape_historical_korea_customs_data(self) -> List[Dict]:
        """한국 관세청 과거 데이터 수집"""
        return self.korea_customs_scraper.scrape_historical_data()
    
    def scrape_historical_trade_statistics(self) -> List[Dict]:
        """과거 무역 통계 데이터 수집"""
        return self.historical_data_scraper.scrape_historical_trade_statistics()
    
    def scrape_un_comtrade_data_yearly(self, years: List[int] = None) -> List[Dict]:
        """특정 연도별 UN Comtrade 데이터 수집"""
        return self.un_comtrade_scraper.scrape_yearly_data(years)
    
    def collect_all_real_data(self) -> Dict:
        """모든 실제 데이터 소스에서 데이터 수집 (시뮬레이션 없음)"""
        logger.info("=== 실제 데이터 수집 시작 ===")
        all_trade_data = []
        collection_stats = {
            'total_collected': 0,
            'sources_used': [],
            'errors': []
        }
        
        try:
            # 각 실제 데이터 소스별로 수집
            data_sources = [
                ('UN_Comtrade', self.scrape_un_comtrade_data),
                ('Korea_Customs', self.scrape_korea_customs_data),
                ('Additional_Sources', self.scrape_additional_real_sources),
                ('Public_Trade_Data', self.scrape_public_trade_data)
            ]
            
            for source_name, scraper_func in data_sources:
                try:
                    logger.info(f"{source_name} 데이터 수집 시작...")
                    source_data = scraper_func()
                    
                    if source_data:
                        # 상세 정보 추가
                        enhanced_data = []
                        for record in source_data:
                            enhanced_record = self.detail_generator.enhance_trade_record(record)
                            enhanced_data.append(enhanced_record)
                        
                        all_trade_data.extend(enhanced_data)
                        collection_stats['sources_used'].append(source_name)
                        logger.info(f"{source_name}에서 {len(source_data)}건 수집")
                    else:
                        logger.warning(f"{source_name}에서 데이터 없음")
                        
                    time.sleep(2)  # 소스간 간격
                    
                except Exception as e:
                    error_msg = f"{source_name} 수집 오류: {e}"
                    logger.error(error_msg)
                    collection_stats['errors'].append(error_msg)
                    continue
            
            collection_stats['total_collected'] = len(all_trade_data)
            
            # 데이터베이스에 저장
            if all_trade_data:
                saved_count = 0
                for trade_record in all_trade_data:
                    try:
                        # TradeRecord 객체 생성
                        record = TradeRecord(
                            product_code=trade_record.get('product_code', ''),
                            product_description=trade_record.get('product_description', ''),
                            country_origin=trade_record.get('country_origin', ''),
                            country_destination=trade_record.get('country_destination', ''),
                            trade_value=float(trade_record.get('trade_value', 0)),
                            quantity=float(trade_record.get('quantity', 0)),
                            trade_type=trade_record.get('trade_type', ''),
                            period=trade_record.get('period', ''),
                            year=int(trade_record.get('year', datetime.now().year)),
                            source=trade_record.get('source', ''),
                            detailed_info=trade_record.get('detailed_info', {})
                        )
                        
                        # 데이터베이스에 저장
                        record_id = self.db.save_trade_record(record)
                        if record_id:
                            saved_count += 1
                            
                    except Exception as e:
                        logger.error(f"데이터 저장 오류: {e}")
                        continue
                
                logger.info(f"총 {saved_count}건 데이터베이스에 저장 완료")
                
                # 텔레그램 알림 발송
                if saved_count > 0:
                    try:
                        # Note: 비동기 함수는 별도 처리 필요
                        logger.info(f"새 데이터 알림: {saved_count}건 수집됨, 소스: {collection_stats['sources_used']}")
                    except Exception as e:
                        logger.error(f"알림 처리 오류: {e}")
            else:
                logger.warning("수집된 실제 데이터 없음")
                
        except Exception as e:
            error_msg = f"실제 데이터 수집 중 오류: {e}"
            logger.error(error_msg)
            collection_stats['errors'].append(error_msg)
            
            try:
                # Note: 비동기 함수는 별도 처리 필요
                logger.error(f"시스템 알림: 데이터 수집 오류: {error_msg}")
            except:
                pass
        
        logger.info("=== 실제 데이터 수집 완료 ===")
        return collection_stats
    
    def collect_historical_data(self) -> Dict:
        """과거 데이터 수집"""
        logger.info("=== 과거 데이터 수집 시작 ===")
        all_historical_data = []
        collection_stats = {
            'total_collected': 0,
            'sources_used': [],
            'errors': []
        }
        
        try:
            # 각 과거 데이터 소스별로 수집
            historical_sources = [
                ('UN_Comtrade_Historical', self.scrape_historical_un_comtrade_data),
                ('Korea_Customs_Historical', self.scrape_historical_korea_customs_data),
                ('Trade_Statistics_Historical', self.scrape_historical_trade_statistics)
            ]
            
            for source_name, scraper_func in historical_sources:
                try:
                    logger.info(f"{source_name} 과거 데이터 수집 시작...")
                    source_data = scraper_func()
                    
                    if source_data:
                        # 상세 정보 추가
                        enhanced_data = []
                        for record in source_data:
                            enhanced_record = self.detail_generator.enhance_trade_record(record)
                            enhanced_data.append(enhanced_record)
                        
                        all_historical_data.extend(enhanced_data)
                        collection_stats['sources_used'].append(source_name)
                        logger.info(f"{source_name}에서 {len(source_data)}건 수집")
                    else:
                        logger.warning(f"{source_name}에서 과거 데이터 없음")
                        
                    time.sleep(3)  # 과거 데이터 수집은 더 긴 간격
                    
                except Exception as e:
                    error_msg = f"{source_name} 수집 오류: {e}"
                    logger.error(error_msg)
                    collection_stats['errors'].append(error_msg)
                    continue
            
            collection_stats['total_collected'] = len(all_historical_data)
            
            # 데이터베이스에 저장
            if all_historical_data:
                saved_count = 0
                for trade_record in all_historical_data:
                    try:
                        record = TradeRecord(
                            product_code=trade_record.get('product_code', ''),
                            product_description=trade_record.get('product_description', ''),
                            country_origin=trade_record.get('country_origin', ''),
                            country_destination=trade_record.get('country_destination', ''),
                            trade_value=float(trade_record.get('trade_value', 0)),
                            quantity=float(trade_record.get('quantity', 0)),
                            trade_type=trade_record.get('trade_type', ''),
                            period=trade_record.get('period', ''),
                            year=int(trade_record.get('year', datetime.now().year)),
                            source=trade_record.get('source', ''),
                            detailed_info=trade_record.get('detailed_info', {})
                        )
                        
                        record_id = self.db.save_trade_record(record)
                        if record_id:
                            saved_count += 1
                            
                    except Exception as e:
                        logger.error(f"과거 데이터 저장 오류: {e}")
                        continue
                
                logger.info(f"총 {saved_count}건 과거 데이터 저장 완료")
            else:
                logger.warning("수집된 과거 데이터 없음")
                
        except Exception as e:
            error_msg = f"과거 데이터 수집 중 오류: {e}"
            logger.error(error_msg)
            collection_stats['errors'].append(error_msg)
        
        logger.info("=== 과거 데이터 수집 완료 ===")
        return collection_stats
    
    def collect_simulation_data_for_testing(self) -> Dict:
        """테스트용 시뮬레이션 데이터 생성 (개발/테스트 전용)"""
        logger.info("=== 테스트용 시뮬레이션 데이터 생성 ===")
        
        if self.is_railway:
            logger.warning("프로덕션 환경에서는 시뮬레이션 데이터를 생성하지 않습니다")
            return {'total_collected': 0, 'sources_used': [], 'errors': ['Production environment - simulation disabled']}
        
        # 이 함수는 기존 시뮬레이션 로직을 유지하되, 명시적으로 테스트 목적임을 표시
        return self.detail_generator.generate_test_simulation_data()
    
    def close(self):
        """리소스 정리"""
        try:
            if self.session:
                self.session.close()
            if self.db:
                self.db.close()
        except Exception as e:
            logger.error(f"리소스 정리 오류: {e}")
