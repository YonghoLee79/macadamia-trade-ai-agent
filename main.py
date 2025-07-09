#!/usr/bin/env python3
"""
마카다미아 무역 데이터 AI 에이전트
전세계 마카다미아 수출입 정보를 매일 수집하고 분석합니다.
"""

import argparse
import logging
from scheduler import MacadamiaTradeScheduler
from ai_agent import MacadamiaTradeAIAgent
from data_scraper import MacadamiaTradeDataScraper

def main():
    parser = argparse.ArgumentParser(description='마카다미아 무역 데이터 AI 에이전트')
    parser.add_argument('--mode', choices=['schedule', 'analyze', 'collect'], 
                       default='schedule', help='실행 모드 선택')
    parser.add_argument('--days', type=int, default=7, 
                       help='분석할 일수 (analyze 모드에서만 사용)')
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    if args.mode == 'schedule':
        # 스케줄러 모드: 매일 자동 실행
        scheduler = MacadamiaTradeScheduler()
        scheduler.start_scheduler()
        
    elif args.mode == 'collect':
        # 데이터 수집만 실행
        logger.info("데이터 수집 모드 실행...")
        scraper = MacadamiaTradeDataScraper()
        trade_data = scraper.collect_all_data()
        scraper.save_to_database(trade_data)
        logger.info(f"데이터 수집 완료: {len(trade_data)}건")
        
    elif args.mode == 'analyze':
        # 분석만 실행
        logger.info(f"최근 {args.days}일 데이터 분석 모드 실행...")
        ai_agent = MacadamiaTradeAIAgent()
        analysis = ai_agent.analyze_trade_trends(args.days)
        print("\n" + "="*50)
        print("마카다미아 무역 동향 분석")
        print("="*50)
        print(analysis)

if __name__ == "__main__":
    main()
