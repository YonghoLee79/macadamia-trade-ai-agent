#!/usr/bin/env python3
"""
ngrok을 사용하여 로컬 서버를 공개 URL로 터널링하는 도구
"""

import subprocess
import time
import requests
import json
import os

def start_ngrok_tunnel(port=5002):
    """ngrok으로 터널 시작"""
    print(f"포트 {port}에 대한 ngrok 터널을 시작합니다...")
    
    try:
        # ngrok 프로세스 시작
        process = subprocess.Popen(
            ["ngrok", "http", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # ngrok이 시작될 때까지 잠시 대기
        time.sleep(3)
        
        # ngrok API로 터널 정보 가져오기
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            tunnels = response.json()
            
            if tunnels.get('tunnels'):
                tunnel = tunnels['tunnels'][0]
                public_url = tunnel['public_url']
                print(f"✅ ngrok 터널이 생성되었습니다!")
                print(f"🌐 공개 URL: {public_url}")
                print(f"🔗 로컬 URL: http://localhost:{port}")
                
                # .env 파일에 공개 URL 저장
                update_env_with_public_url(public_url)
                
                return public_url, process
            else:
                print("❌ ngrok 터널을 찾을 수 없습니다.")
                return None, process
                
        except requests.exceptions.ConnectionError:
            print("❌ ngrok API에 연결할 수 없습니다. ngrok이 설치되어 있는지 확인하세요.")
            return None, process
            
    except FileNotFoundError:
        print("❌ ngrok이 설치되어 있지 않습니다.")
        print("설치 방법:")
        print("1. https://ngrok.com/download 에서 다운로드")
        print("2. 또는 Homebrew: brew install ngrok")
        return None, None

def update_env_with_public_url(public_url):
    """공개 URL을 .env 파일에 저장"""
    env_file = ".env"
    
    # 기존 .env 파일 읽기
    env_lines = []
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            env_lines = f.readlines()
    
    # PUBLIC_URL 라인 찾기 또는 추가
    found = False
    for i, line in enumerate(env_lines):
        if line.startswith('PUBLIC_URL='):
            env_lines[i] = f"PUBLIC_URL={public_url}\n"
            found = True
            break
    
    if not found:
        env_lines.append(f"PUBLIC_URL={public_url}\n")
    
    # .env 파일 업데이트
    with open(env_file, 'w') as f:
        f.writelines(env_lines)
    
    print(f"✅ .env 파일에 PUBLIC_URL이 업데이트되었습니다: {public_url}")

def check_ngrok_status():
    """현재 ngrok 상태 확인"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        tunnels = response.json()
        
        if tunnels.get('tunnels'):
            for tunnel in tunnels['tunnels']:
                print(f"🌐 활성 터널: {tunnel['public_url']} -> {tunnel['config']['addr']}")
        else:
            print("📭 활성 터널이 없습니다.")
            
    except requests.exceptions.ConnectionError:
        print("❌ ngrok이 실행되지 않고 있습니다.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            check_ngrok_status()
        elif sys.argv[1] == "start":
            port = int(sys.argv[2]) if len(sys.argv) > 2 else 5002
            public_url, process = start_ngrok_tunnel(port)
            if public_url:
                print(f"\n🚀 터널이 활성화되었습니다!")
                print(f"이제 텔레그램 메시지의 링크가 작동합니다.")
                print(f"Ctrl+C를 눌러 종료하세요.")
                try:
                    process.wait()
                except KeyboardInterrupt:
                    print("\n터널을 종료합니다...")
                    process.terminate()
    else:
        print("사용법:")
        print("  python ngrok_tunnel.py start [포트번호]  # 터널 시작 (기본: 5002)")
        print("  python ngrok_tunnel.py status           # 현재 상태 확인")
