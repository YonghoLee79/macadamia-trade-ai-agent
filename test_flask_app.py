"""
모듈화된 Flask 앱 실행 테스트
"""
import time
import threading
import requests
from app import app

def test_flask_app():
    """Flask 앱 간단 실행 테스트"""
    print("=== Flask 앱 실행 테스트 ===")
    
    # Flask 앱을 백그라운드에서 실행
    def run_app():
        app.run(debug=False, host='127.0.0.1', port=5001, use_reloader=False)
    
    # 백그라운드 스레드로 앱 시작
    app_thread = threading.Thread(target=run_app, daemon=True)
    app_thread.start()
    
    # 앱이 시작할 시간을 줌
    time.sleep(3)
    
    try:
        # 헬스체크 엔드포인트 테스트
        response = requests.get('http://127.0.0.1:5001/health', timeout=5)
        if response.status_code == 200:
            print("✓ 헬스체크 엔드포인트 정상 작동")
            print(f"  응답: {response.json()}")
        else:
            print(f"✗ 헬스체크 실패: {response.status_code}")
            
        # 대시보드 API 테스트
        response = requests.get('http://127.0.0.1:5001/api/dashboard', timeout=5)
        if response.status_code == 200:
            print("✓ 대시보드 API 정상 작동")
        else:
            print(f"! 대시보드 API 응답: {response.status_code}")
            
        # 상태 API 테스트
        response = requests.get('http://127.0.0.1:5001/api/status', timeout=5)
        if response.status_code == 200:
            print("✓ 상태 API 정상 작동")
        else:
            print(f"! 상태 API 응답: {response.status_code}")
            
        print("\n✅ Flask 앱 기본 테스트 완료!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ 요청 오류: {e}")
        return False
    except Exception as e:
        print(f"✗ 테스트 오류: {e}")
        return False

if __name__ == "__main__":
    success = test_flask_app()
    if success:
        print("\n🎉 Flask 앱 테스트 성공!")
    else:
        print("\n❌ Flask 앱 테스트 실패!")
        
    # 테스트 완료 후 약간 대기
    time.sleep(2)
