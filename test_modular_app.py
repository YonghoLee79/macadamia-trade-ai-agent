"""
모듈화된 애플리케이션 테스트 스크립트
"""
import sys
import os
import requests
import time

def test_modular_app():
    """모듈화된 Flask 애플리케이션 테스트"""
    print("=== 모듈화된 애플리케이션 테스트 ===")
    
    # 1. 임포트 테스트
    try:
        print("1. 모듈 임포트 테스트...")
        from web import (
            create_app, create_components,
            DataAPIHandler, AIAPIHandler, ProductAPIHandler, ReportAPIHandler,
            DashboardAPI, TelegramAPI, DatabaseAPI, HealthAPI
        )
        print("✓ 모든 모듈 임포트 성공")
    except ImportError as e:
        print(f"✗ 임포트 오류: {e}")
        return False
    
    # 2. 컴포넌트 생성 테스트
    try:
        print("\n2. 컴포넌트 생성 테스트...")
        components = create_components()
        print(f"✓ DB Manager: {type(components['db_manager'])}")
        print(f"✓ Scraper: {type(components['scraper'])}")
        print(f"✓ Config: {type(components['config'])}")
        if components['ai_agent']:
            print(f"✓ AI Agent: {type(components['ai_agent'])}")
        else:
            print("! AI Agent: None (OpenAI API key not configured)")
    except Exception as e:
        print(f"✗ 컴포넌트 생성 오류: {e}")
        return False
    
    # 3. API 핸들러 생성 테스트
    try:
        print("\n3. API 핸들러 생성 테스트...")
        data_api = DataAPIHandler(components)
        ai_api = AIAPIHandler(components)
        product_api = ProductAPIHandler(components)
        report_api = ReportAPIHandler(components)
        dashboard_api = DashboardAPI(components['db_manager'])
        telegram_api = TelegramAPI(components['db_manager'])
        database_api = DatabaseAPI(components['db_manager'], components['config'])
        health_api = HealthAPI()
        print("✓ 모든 API 핸들러 생성 성공")
    except Exception as e:
        print(f"✗ API 핸들러 생성 오류: {e}")
        return False
    
    # 4. Flask 앱 생성 테스트
    try:
        print("\n4. Flask 앱 생성 테스트...")
        app = create_app()
        print(f"✓ Flask 앱 생성 성공: {type(app)}")
    except Exception as e:
        print(f"✗ Flask 앱 생성 오류: {e}")
        return False
    
    # 5. 스크래퍼 모듈 테스트
    try:
        print("\n5. 스크래퍼 모듈 테스트...")
        scraper = components['scraper']
        
        # 각 스크래퍼 메서드 확인
        methods = [
            'scrape_un_comtrade_data',
            'scrape_korea_customs_data', 
            'scrape_additional_real_sources',
            'scrape_public_trade_data'
        ]
        
        for method in methods:
            if hasattr(scraper, method):
                print(f"✓ {method} 메서드 존재")
            else:
                print(f"✗ {method} 메서드 없음")
                
    except Exception as e:
        print(f"✗ 스크래퍼 모듈 테스트 오류: {e}")
        return False
    
    print("\n=== 모든 테스트 완료 ===")
    return True

if __name__ == "__main__":
    success = test_modular_app()
    if success:
        print("\n🎉 모듈화 테스트 성공!")
        sys.exit(0)
    else:
        print("\n❌ 모듈화 테스트 실패!")
        sys.exit(1)
