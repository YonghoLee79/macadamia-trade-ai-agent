#!/usr/bin/env python3
"""
지난 1년간의 마카다미아 무역 시뮬레이션 데이터를 생성하고 분석하는 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_scraper import MacadamiaTradeDataScraper
from ai_agent import MacadamiaTradeAIAgent
from config import Config
import logging
from datetime import datetime, timedelta
import random

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_sample_trade_data():
    """지난 1년간의 마카다미아 무역 시뮬레이션 데이터 생성"""
    
    # 주요 마카다미아 무역 국가들
    exporters = [
        'Australia', 'South Africa', 'Kenya', 'New Zealand', 
        'Guatemala', 'Hawaii (USA)', 'Brazil', 'Malawi'
    ]
    
    importers = [
        'Korea, Republic of', 'Japan', 'China', 'United States', 
        'Germany', 'United Kingdom', 'France', 'Netherlands'
    ]
    
    companies_export = [
        'Australian Macadamia Society', 'Royal Macadamia', 'Golden Macadamia',
        'SA Premium Nuts', 'Kenya Nut Company', 'NZ Macadamia Co.',
        'Premium Nuts Ltd', 'African Macadamia Export'
    ]
    
    companies_import = [
        'Korean Food Trading', 'Asia Pacific Foods', 'Premium Nuts Import',
        'Global Nut Distributors', 'European Macadamia', 'Gourmet Imports',
        'Healthy Nuts Co.', 'International Food Trade'
    ]
    
    # 12개월간의 무역 데이터 생성
    trade_data = []
    base_date = datetime.now() - timedelta(days=365)
    
    for month in range(12):
        month_date = base_date + timedelta(days=30 * month)
        
        # 월별 30-50건의 거래 생성
        monthly_trades = random.randint(30, 50)
        
        for _ in range(monthly_trades):
            exporter = random.choice(exporters)
            importer = random.choice(importers)
            
            # 한국 관련 거래는 더 자주 생성
            if random.random() < 0.3:
                importer = 'Korea, Republic of'
            
            trade_record = {
                'date': month_date.date(),
                'country_origin': exporter,
                'country_destination': importer,
                'company_exporter': random.choice(companies_export),
                'company_importer': random.choice(companies_import),
                'product_code': random.choice(['080250', '080251']),
                'product_description': 'Macadamia nuts' + (' in shell' if random.random() < 0.5 else ' shelled'),
                'quantity': round(random.uniform(1000, 50000), 2),  # kg
                'value_usd': round(random.uniform(10000, 500000), 2),  # USD
                'trade_type': 'export'
            }
            
            trade_data.append(trade_record)
    
    return trade_data

def analyze_trade_data(data):
    """무역 데이터 상세 분석"""
    if not data:
        print("❌ 분석할 데이터가 없습니다.")
        return
    
    print(f"\n📊 지난 1년간 마카다미아 무역 데이터 분석 결과")
    print("=" * 60)
    
    # 기본 통계
    total_trades = len(data)
    total_value = sum(float(record['value_usd']) for record in data)
    total_quantity = sum(float(record['quantity']) for record in data)
    avg_price_per_kg = total_value / total_quantity if total_quantity > 0 else 0
    
    print(f"📈 전체 통계:")
    print(f"  • 총 거래 건수: {total_trades:,}건")
    print(f"  • 총 거래 가치: ${total_value:,.2f}")
    print(f"  • 총 거래 수량: {total_quantity:,.2f} kg")
    print(f"  • 평균 단가: ${avg_price_per_kg:.2f}/kg")
    
    # 국가별 분석
    export_countries = {}
    import_countries = {}
    
    for record in data:
        origin = record['country_origin']
        destination = record['country_destination']
        value = float(record['value_usd'])
        
        if origin in export_countries:
            export_countries[origin]['count'] += 1
            export_countries[origin]['value'] += value
        else:
            export_countries[origin] = {'count': 1, 'value': value}
            
        if destination in import_countries:
            import_countries[destination]['count'] += 1
            import_countries[destination]['value'] += value
        else:
            import_countries[destination] = {'count': 1, 'value': value}
    
    # 상위 수출국
    print(f"\n🌍 주요 수출국 (거래액 기준):")
    sorted_exporters = sorted(export_countries.items(), key=lambda x: x[1]['value'], reverse=True)
    for i, (country, stats) in enumerate(sorted_exporters[:5], 1):
        print(f"  {i}. {country}: ${stats['value']:,.2f} ({stats['count']:,}건)")
    
    # 상위 수입국
    print(f"\n🏭 주요 수입국 (거래액 기준):")
    sorted_importers = sorted(import_countries.items(), key=lambda x: x[1]['value'], reverse=True)
    for i, (country, stats) in enumerate(sorted_importers[:5], 1):
        print(f"  {i}. {country}: ${stats['value']:,.2f} ({stats['count']:,}건)")
    
    # 한국 관련 분석
    korea_trades = [r for r in data if r['country_destination'] == 'Korea, Republic of']
    if korea_trades:
        korea_value = sum(float(r['value_usd']) for r in korea_trades)
        korea_quantity = sum(float(r['quantity']) for r in korea_trades)
        print(f"\n🇰🇷 한국 수입 분석:")
        print(f"  • 수입 건수: {len(korea_trades):,}건")
        print(f"  • 수입 가치: ${korea_value:,.2f}")
        print(f"  • 수입 수량: {korea_quantity:,.2f} kg")
        print(f"  • 전체 대비 비중: {len(korea_trades)/total_trades*100:.1f}%")
        
        # 한국의 주요 공급국
        korea_suppliers = {}
        for trade in korea_trades:
            supplier = trade['country_origin']
            if supplier in korea_suppliers:
                korea_suppliers[supplier] += float(trade['value_usd'])
            else:
                korea_suppliers[supplier] = float(trade['value_usd'])
        
        print(f"  • 주요 공급국:")
        sorted_suppliers = sorted(korea_suppliers.items(), key=lambda x: x[1], reverse=True)
        for i, (country, value) in enumerate(sorted_suppliers[:3], 1):
            print(f"    {i}. {country}: ${value:,.2f}")
    
    # 월별 트렌드 분석
    monthly_stats = {}
    for record in data:
        month_key = record['date'].strftime('%Y-%m')
        value = float(record['value_usd'])
        
        if month_key in monthly_stats:
            monthly_stats[month_key]['count'] += 1
            monthly_stats[month_key]['value'] += value
        else:
            monthly_stats[month_key] = {'count': 1, 'value': value}
    
    print(f"\n📅 월별 거래 동향:")
    sorted_months = sorted(monthly_stats.items())
    for month, stats in sorted_months[-6:]:  # 최근 6개월
        print(f"  {month}: {stats['count']:,}건, ${stats['value']:,.0f}")

def main():
    """메인 실행 함수"""
    print("🥥 마카다미아 무역 데이터 분석 시스템")
    print("=" * 60)
    
    try:
        # 1. 시뮬레이션 데이터 생성
        print("\n📊 지난 1년간 무역 데이터 생성 중...")
        trade_data = generate_sample_trade_data()
        print(f"✅ {len(trade_data)}건의 무역 데이터 생성 완료")
        
        # 2. 데이터베이스에 저장
        print("\n💾 데이터베이스에 저장 중...")
        scraper = MacadamiaTradeDataScraper()
        saved_count = scraper.save_to_database(trade_data)
        print(f"✅ {saved_count}건 저장 완료")
        
        # 3. 상세 분석
        analyze_trade_data(trade_data)
        
        # 4. AI 분석
        print(f"\n🤖 AI 분석 시작...")
        try:
            ai_agent = MacadamiaTradeAIAgent()
            analysis = ai_agent.analyze_trade_trends(365)
            print("✅ AI 분석 완료")
            print(f"\n🔍 AI 분석 결과:")
            print("-" * 40)
            print(analysis)
        except Exception as e:
            print(f"⚠️ AI 분석 실패: {e}")
        
        print(f"\n🎉 지난 1년간 마카다미아 무역 데이터 분석 완료!")
        print(f"\n📱 웹 대시보드에서 더 자세한 분석을 확인하세요:")
        print(f"   https://macadamia-trade-ai-agent-production.up.railway.app/")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        logger.error(f"분석 실행 오류: {e}")

if __name__ == "__main__":
    main()
