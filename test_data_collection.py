#!/usr/bin/env python3
"""
데이터 수집 테스트 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_scraper import MacadamiaTradeDataScraper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_data_collection():
    """데이터 수집 기능 테스트"""
    try:
        scraper = MacadamiaTradeDataScraper()
        
        print("🔍 데이터 수집 테스트 시작...")
        
        # 데이터 수집 실행
        result = scraper.collect_and_notify()
        
        if result['success']:
            print(f"✅ 데이터 수집 성공!")
            print(f"   - 수집된 데이터: {result['collected']}건")
            print(f"   - 저장된 데이터: {result['saved']}건")
            print(f"   - 소요 시간: {result['duration']:.1f}초")
        else:
            print(f"❌ 데이터 수집 실패: {result.get('error', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        print(f"❌ 테스트 실행 오류: {e}")
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    test_data_collection()
