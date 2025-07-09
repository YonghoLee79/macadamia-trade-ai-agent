#!/usr/bin/env python3

import asyncio
from telegram import Bot
from config import Config

async def send_final_test():
    config = Config()
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    
    message = f'''🎯 최종 링크 테스트

📊 마카다미아 무역 AI 에이전트 대시보드

🌐 공개 URL: {config.get_dashboard_url()}

🔗 <a href="{config.get_dashboard_url()}">여기를 클릭하여 대시보드 접속</a>

✅ 이제 텔레그램에서 링크 클릭이 가능합니다!
📱 모바일/데스크톱 모두 접속 가능
🚀 ngrok 터널을 통한 실시간 접속'''
    
    await bot.send_message(
        chat_id=config.TELEGRAM_CHAT_ID,
        text=message,
        parse_mode='HTML'
    )

if __name__ == "__main__":
    asyncio.run(send_final_test())
