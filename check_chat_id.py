#!/usr/bin/env python3
"""
텔레그램 Chat ID 확인 스크립트
"""

import requests
import json

def get_chat_id(bot_token):
    """텔레그램 봇의 업데이트를 통해 Chat ID를 확인합니다"""
    
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['ok']:
            print("=== 텔레그램 업데이트 정보 ===")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if data['result']:
                for update in data['result']:
                    if 'message' in update:
                        chat = update['message']['chat']
                        print(f"\n📱 Chat ID: {chat['id']}")
                        print(f"📱 Chat Type: {chat['type']}")
                        if 'username' in chat:
                            print(f"📱 Username: @{chat['username']}")
                        if 'first_name' in chat:
                            print(f"📱 Name: {chat['first_name']}")
            else:
                print("\n⚠️  업데이트가 없습니다.")
                print("봇과 대화를 시작하려면:")
                print("1. 봇을 찾아서 채팅 시작")
                print("2. /start 명령어 전송")
                print("3. 이 스크립트를 다시 실행")
        else:
            print(f"❌ 오류: {data.get('description', '알 수 없는 오류')}")
            
    except Exception as e:
        print(f"❌ 요청 오류: {e}")

if __name__ == "__main__":
    # 현재 .env 파일의 토큰 사용
    bot_token = "7810519361:AAHj6LhrJ01tkwO4G17nFHb0dYUdReKFiTw"
    get_chat_id(bot_token)
