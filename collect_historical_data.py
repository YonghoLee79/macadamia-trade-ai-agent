#!/usr/bin/env python3
"""
지난 1년간의 마카다미아 무역 데이터를 수집하고 분석하는 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_scraper import MacadamiaTradeDataScraper
from ai_agent import MacadamiaTradeAIAgent
from config import Config
import logging
from datetime import datetime, timedelta

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """지난 1년간 데이터 수집 및 분석"""
    print("🔍 지난 1년간 마카다미아 무역 데이터 수집 및 분석 시작...")
    print("=" * 60)
    
    try:
        # 1. 데이터 수집기 초기화
        scraper = MacadamiaTradeDataScraper()
        
        # 2. 지난 1년간 데이터 수집 (2023-2024)
        print("\n📊 UN Comtrade에서 지난 1년간 데이터 수집 중...")
        yearly_data = scraper.scrape_un_comtrade_data_yearly([2023, 2024])
        
        print(f"✅ 수집 완료: {len(yearly_data)}건의 무역 데이터")
        
        # 3. 데이터베이스에 저장
        print("\n💾 데이터베이스에 저장 중...")
        saved_count = scraper.save_to_database(yearly_data)
        print(f"✅ 저장 완료: {saved_count}건")
        
        # 4. 데이터 요약 분석
        print("\n📈 데이터 요약 분석:")
        analyze_collected_data(yearly_data)
        
        # 5. AI 분석 (OpenAI API 키가 있는 경우)
        try:
            print("\n🤖 AI 분석 시작...")
            ai_agent = MacadamiaTradeAIAgent()
            analysis = ai_agent.analyze_trade_trends(365)  # 365일 분석
            print("✅ AI 분석 완료")
            print(f"📊 분석 결과:\n{analysis}")
        except Exception as e:
            print(f"⚠️ AI 분석 실패: {e}")
        
        print("\n🎉 지난 1년간 데이터 수집 및 분석 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        logger.error(f"데이터 수집 실행 오류: {e}")

def analyze_collected_data(data):
    """수집된 데이터 기본 분석"""
    if not data:
        print("❌ 분석할 데이터가 없습니다.")
        return
    
    # 국가별 분석
    countries = {}
    trade_types = {'export': 0, 'import': 0}
    total_value = 0
    total_quantity = 0
    
    for record in data:
        # 국가별 집계
        origin = record.get('country_origin', 'Unknown')
        if origin in countries:
            countries[origin] += 1
        else:
            countries[origin] = 1
        
        # 무역 유형별 집계
        trade_type = record.get('trade_type', '')
        if trade_type in trade_types:
            trade_types[trade_type] += 1
        
        # 총 가치 및 수량
        total_value += float(record.get('trade_value', 0))
        total_quantity += float(record.get('quantity', 0))
    
    # 결과 출력
    print(f"  📊 총 거래 건수: {len(data):,}건")
    print(f"  💰 총 거래 가치: ${total_value:,.2f}")
    print(f"  📦 총 거래 수량: {total_quantity:,.2f} kg")
    print(f"  📤 수출: {trade_types['export']:,}건")
    print(f"  📥 수입: {trade_types['import']:,}건")
    
    print(f"\n  🌍 주요 거래 국가 (상위 10개):")
    sorted_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)
    for i, (country, count) in enumerate(sorted_countries[:10], 1):
        print(f"    {i:2d}. {country}: {count:,}건")

if __name__ == "__main__":
    main()
