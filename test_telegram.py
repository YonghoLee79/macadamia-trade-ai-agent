#!/usr/bin/env python3
"""
텔레그램 알림 테스트 스크립트
"""

from telegram_notifier import send_system_alert, send_new_data_alert
from models import TradeRecord, DatabaseManager
from config import Config

def test_telegram_notifications():
    """텔레그램 알림 기능을 테스트합니다"""
    
    print("=== 마카다미아 무역 AI 에이전트 텔레그램 테스트 ===\n")
    
    # 1. 시스템 알림 테스트
    print("1. 시스템 알림 테스트...")
    result = send_system_alert("INFO", "🥜 마카다미아 무역 AI 에이전트 테스트 메시지입니다!")
    print(f"   결과: {'성공' if result else '실패'}\n")
    
    # 2. 데이터베이스에서 최신 데이터 가져오기
    print("2. 최신 무역 데이터 가져오기...")
    config = Config()
    db_manager = DatabaseManager(config.DATABASE_URL)
    latest_records = db_manager.get_latest_records(days=1)
    
    if latest_records:
        print(f"   최신 {len(latest_records)}개 거래 발견")
        
        # 3. 신규 데이터 알림 테스트
        print("3. 신규 데이터 알림 테스트...")
        
        # TradeRecord를 딕셔너리로 변환
        records_data = []
        for record in latest_records:
            records_data.append({
                'country_origin': record.country_origin,
                'country_destination': record.country_destination,
                'value_usd': record.value_usd,
                'quantity': record.quantity,
                'product_description': record.product_description
            })
        
        result = send_new_data_alert(records_data)
        print(f"   결과: {'성공' if result else '실패'}\n")
    else:
        print("   최신 데이터가 없습니다.\n")
    
    print("=== 테스트 완료 ===")

if __name__ == "__main__":
    test_telegram_notifications()
