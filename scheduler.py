import schedule
import time
import logging
from datetime import datetime
from data_scraper import MacadamiaTradeDataScraper
from ai_agent import MacadamiaTradeAIAgent
from config import Config
from telegram_notifier import send_daily_summary, send_system_alert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MacadamiaTradeScheduler:
    def __init__(self):
        self.scraper = MacadamiaTradeDataScraper()
        self.ai_agent = MacadamiaTradeAIAgent()
        self.config = Config()
    
    def daily_data_collection_job(self):
        """일일 데이터 수집 작업"""
        logger.info("일일 마카다미아 무역 데이터 수집 시작...")
        
        try:
            # 데이터 수집 (알림 포함)
            result = self.scraper.collect_and_notify()
            
            if result['success']:
                logger.info(f"수집된 데이터: {result['collected']}건, 저장: {result['saved']}건")
                
                # AI 분석 및 보고서 생성
                report = self.ai_agent.generate_daily_report()
                
                # 보고서 저장
                self.save_daily_report(report)
                
                # 일일 요약 데이터 생성
                summary_data = self._generate_daily_summary()
                
                # 텔레그램으로 일일 요약 전송
                send_daily_summary(summary_data)
                
                logger.info("일일 작업 완료")
            else:
                logger.error(f"데이터 수집 실패: {result.get('error', 'Unknown error')}")
            
        except Exception as e:
            logger.error(f"일일 작업 실행 중 오류: {e}")
            send_system_alert('error', f"일일 작업 실행 중 오류: {str(e)}")
    
    def _generate_daily_summary(self) -> dict:
        """일일 요약 데이터 생성"""
        try:
            # 오늘 데이터 가져오기
            records = self.scraper.db.get_latest_records(1)
            
            total_records = len(records)
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
                'total_records': total_records,
                'total_value': total_value,
                'top_countries': top_countries,
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            logger.error(f"일일 요약 생성 오류: {e}")
            return {
                'total_records': 0,
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
