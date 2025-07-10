#!/usr/bin/env python3
"""
Railway 배포 후 PUBLIC_URL 업데이트 스크립트
"""

import os
import sys
from config import update_public_url

def main():
    if len(sys.argv) != 2:
        print("사용법: python update_railway_url.py <railway-app-url>")
        print("예시: python update_railway_url.py https://macadamia-trade-production.railway.app")
        sys.exit(1)
    
    new_url = sys.argv[1]
    
    # URL 형식 검증
    if not new_url.startswith('https://') or 'railway.app' not in new_url:
        print("❌ 올바른 Railway URL을 입력하세요 (https://...railway.app)")
        sys.exit(1)
    
    try:
        # PUBLIC_URL 업데이트
        update_public_url(new_url)
        print(f"✅ PUBLIC_URL이 업데이트되었습니다: {new_url}")
        
        # Railway 환경변수도 업데이트하라는 안내
        print("\n📝 다음 단계:")
        print("1. Railway 대시보드 → Variables에서 PUBLIC_URL 환경변수를 다음으로 업데이트:")
        print(f"   PUBLIC_URL={new_url}")
        print("2. Railway에서 앱을 재배포하세요")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
