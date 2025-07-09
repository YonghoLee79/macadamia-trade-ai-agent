#!/usr/bin/env python3
"""
간단한 텔레그램 링크 테스트
"""

import asyncio
from telegram import Bot
from config import Config

async def test_telegram_link():
    """텔레그램 링크 테스트"""
    config = Config()
    
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    
    test_message = f'''🎉 텔레그램 링크 테스트

📊 마카다미아 무역 대시보드가 공개 URL로 업데이트되었습니다!

🌐 공개 URL: {config.get_dashboard_url()}

🔗 <a href="{config.get_dashboard_url()}">대시보드에서 자세히 보기</a>

이제 텔레그램에서 링크를 클릭하면 대시보드로 이동할 수 있습니다! 🚀

✅ ngrok 터널을 통해 로컬 서버에 접근 가능
📱 모바일에서도 접속 가능'''

    try:
        await bot.send_message(
            chat_id=config.TELEGRAM_CHAT_ID,
            text=test_message,
            parse_mode='HTML'
        )
        print("✅ 텔레그램 링크 테스트 메시지 전송 완료!")
        print(f"🌐 공개 대시보드 URL: {config.get_dashboard_url()}")
        print("📱 텔레그램에서 링크를 클릭해보세요!")
        
    except Exception as e:
        print(f"❌ 메시지 전송 오류: {e}")

if __name__ == "__main__":
    asyncio.run(test_telegram_link())
