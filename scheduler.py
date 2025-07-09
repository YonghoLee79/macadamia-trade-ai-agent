import schedule
import time
import logging
from datetime import datetime
from data_scraper import MacadamiaTradeDataScraper
from ai_agent import MacadamiaTradeAIAgent
from excel_reporter import MacadamiaTradeExcelReporter
from config import Config
from telegram_notifier import send_daily_summary, send_system_alert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MacadamiaTradeScheduler:
    def __init__(self):
        self.scraper = MacadamiaTradeDataScraper()
        self.ai_agent = MacadamiaTradeAIAgent()
        self.excel_reporter = MacadamiaTradeExcelReporter()
        self.config = Config()
    
    def daily_data_collection_job(self):
        """일일 데이터 수집 작업 - 과거 1년간 데이터 확인 및 신규 정보 알림"""
        logger.info("일일 마카다미아 무역 데이터 수집 시작 (과거 1년간 데이터 확인)...")
        
        try:
            # 과거 1년간 데이터 수집 및 중복 제거 (알림 포함)
            result = self.scraper.collect_historical_data_and_notify()
            
            if result['success']:
                logger.info(f"전체 확인: {result['total_checked']}건, 신규 발견: {result['new_found']}건, 저장: {result['saved']}건")
                
                # 신규 데이터가 있는 경우에만 AI 분석 수행
                if result['saved'] > 0:
                    # AI 분석 및 보고서 생성
                    report = self.ai_agent.generate_daily_report()
                    
                    # 마크다운 보고서 저장
                    self.save_daily_report(report)
                    
                    # 엑셀 보고서 생성
                    excel_filename = self.excel_reporter.generate_daily_excel_report()
                    if excel_filename:
                        logger.info(f"엑셀 보고서 생성 완료: {excel_filename}")
                        
                        # 비교 분석 보고서도 생성
                        comparison_filename = self.excel_reporter.create_comparison_report(7)
                        if comparison_filename:
                            logger.info(f"비교 분석 보고서 생성 완료: {comparison_filename}")
                    
                    # 일일 요약 데이터 생성
                    summary_data = self._generate_daily_summary(result)
                    
                    # 텔레그램으로 일일 요약 전송 (엑셀 파일 정보 포함)
                    summary_data['excel_report'] = excel_filename
                    summary_data['comparison_report'] = comparison_filename
                    send_daily_summary(summary_data)
                else:
                    logger.info("신규 데이터가 없어 분석을 건너뜁니다.")
                
                logger.info("일일 작업 완료")
            else:
                logger.error(f"데이터 수집 실패: {result.get('error', 'Unknown error')}")
                send_system_alert('error', f"데이터 수집 실패: {result.get('error', 'Unknown error')}")
            
        except Exception as e:
            logger.error(f"일일 작업 실행 중 오류: {e}")
            send_system_alert('error', f"일일 작업 실행 중 오류: {str(e)}")
    
    def _generate_daily_summary(self, collection_result: dict = None) -> dict:
        """일일 요약 데이터 생성"""
        try:
            # 오늘 새로 추가된 데이터 정보
            if collection_result:
                new_records_count = collection_result.get('saved', 0)
                total_checked = collection_result.get('total_checked', 0)
            else:
                new_records_count = 0
                total_checked = 0
            
            # 최근 1일 데이터 가져오기
            records = self.scraper.db.get_latest_records(1)
            
            total_value = sum(record.value_usd or 0 for record in records)
            
            # 국가별 집계
            country_stats = {}
            for record in records:
                country = record.country_origin
                if country not in country_stats:
                    country_stats[country] = {'value': 0, 'count': 0}
                country_stats[country]['value'] += record.value_usd or 0
                country_stats[country]['count'] += 1
            
            # 상위 국가
            top_countries = sorted(country_stats.items(), key=lambda x: x[1]['value'], reverse=True)[:5]
            
            return {
                'total_records': len(records),
                'new_records_today': new_records_count,
                'total_checked': total_checked,
                'total_value': total_value,
                'top_countries': top_countries,
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            logger.error(f"일일 요약 생성 오류: {e}")
            return {
                'total_records': 0,
                'new_records_today': 0,
                'total_checked': 0,
                'total_value': 0,
                'top_countries': [],
                'date': datetime.now().strftime('%Y-%m-%d')
            }
    
    def save_daily_report(self, report: str):
        """일일 보고서를 파일로 저장"""
        filename = f"reports/macadamia_report_{datetime.now().strftime('%Y%m%d')}.md"
        
        import os
        os.makedirs("reports", exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"보고서 저장: {filename}")
    
    def start_scheduler(self):
        """스케줄러 시작"""
        logger.info("마카다미아 무역 AI 에이전트 스케줄러 시작...")
        
        # 매일 지정된 시간에 실행
        schedule.every().day.at(self.config.UPDATE_SCHEDULE).do(
            self.daily_data_collection_job
        )
        
        # 테스트용: 즉시 실행
        # self.daily_data_collection_job()
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크
    
    def test_historical_collection(self):
        """과거 1년간 데이터 수집 테스트 (즉시 실행)"""
        logger.info("과거 1년간 데이터 수집 테스트 시작...")
        return self.daily_data_collection_job()
