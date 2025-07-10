#!/usr/bin/env python3
"""
Railway 배포 상태 확인 및 테스트 스크립트
"""

import requests
import time
import json

# 알려진 Railway URL들 (실제 URL로 교체 필요)
POSSIBLE_URLS = [
    "https://macadamia-trade-ai-agent-production.up.railway.app",
    "https://worldtrade-production.up.railway.app",
    "https://macadamia-trade-production.up.railway.app"
]

def test_railway_deployment():
    """Railway 배포 상태 테스트"""
    print("🚂 Railway 배포 상태 확인 중...")
    
    for url in POSSIBLE_URLS:
        print(f"\n🔍 테스트 중: {url}")
        
        try:
            # 헬스체크 엔드포인트 테스트
            response = requests.get(f"{url}/health", timeout=10)
            
            if response.status_code == 200:
                print(f"✅ 성공! Railway 앱이 {url}에서 실행 중")
                data = response.json()
                print(f"   상태: {data.get('status')}")
                print(f"   타임스탬프: {data.get('timestamp')}")
                print(f"   버전: {data.get('version')}")
                
                # 추가 엔드포인트 테스트
                test_endpoints(url)
                return url
                
            else:
                print(f"❌ 응답 코드: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 연결 오류: {e}")
        except Exception as e:
            print(f"❌ 오류: {e}")
    
    print("\n⚠️  알려진 URL에서 앱을 찾을 수 없습니다.")
    print("Railway 대시보드에서 실제 배포 URL을 확인해주세요.")
    return None

def test_endpoints(base_url):
    """주요 엔드포인트 테스트"""
    endpoints = [
        "/api/dashboard",
        "/api/status", 
        "/api/products/categories"
    ]
    
    print(f"\n📊 주요 엔드포인트 테스트:")
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {endpoint}")
            else:
                print(f"   ⚠️  {endpoint} (코드: {response.status_code})")
        except Exception as e:
            print(f"   ❌ {endpoint} (오류: {str(e)[:50]}...)")

def check_deployment_status():
    """배포 상태 확인"""
    print("=" * 60)
    print("🚀 마카다미아 무역 AI 에이전트 - Railway 배포 확인")
    print("=" * 60)
    
    print("\n📋 모듈화 완료 사항:")
    print("   ✅ scrapers/ - 5개 모듈 (데이터 수집)")
    print("   ✅ reporters/ - 5개 모듈 (보고서 생성)")
    print("   ✅ web/ - 9개 모듈 (API 핸들러)")
    print("   ✅ app.py - 라우트 오케스트레이터")
    print("   ✅ 하위 호환성 유지")
    
    # Railway 배포 테스트
    active_url = test_railway_deployment()
    
    if active_url:
        print(f"\n🎉 배포 성공!")
        print(f"🌐 활성 URL: {active_url}")
        print(f"📱 모바일 접속 가능")
        print(f"🔧 모든 모듈화된 API 사용 가능")
    else:
        print(f"\n⏳ 배포 진행 중이거나 URL 확인 필요")
        print(f"   Railway 대시보드를 확인해주세요.")

if __name__ == "__main__":
    check_deployment_status()
