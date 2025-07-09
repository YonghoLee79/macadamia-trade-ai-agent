import schedule
import time
import logging
from datetime import datetime
from data_scraper import MacadamiaTradeDataScraper
from ai_agent import MacadamiaTradeAIAgent
from config import Config

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
            # 데이터 수집
            trade_data = self.scraper.collect_all_data()
            logger.info(f"수집된 데이터: {len(trade_data)}건")
            
            # 데이터베이스 저장
            self.scraper.save_to_database(trade_data)
            logger.info("데이터베이스 저장 완료")
            
            # AI 분석 및 보고서 생성
            report = self.ai_agent.generate_daily_report()
            
            # 보고서 저장
            self.save_daily_report(report)
            
            logger.info("일일 작업 완료")
            
        except Exception as e:
            logger.error(f"일일 작업 실행 중 오류: {e}")
    
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
