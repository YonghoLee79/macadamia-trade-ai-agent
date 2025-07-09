import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Optional
from telegram import Bot
from telegram.error import TelegramError
from config import Config

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        self.config = Config()
        self.bot_token = self.config.TELEGRAM_BOT_TOKEN
        self.chat_id = self.config.TELEGRAM_CHAT_ID
        self.bot = None
        
        if self.bot_token and self.chat_id:
            self.bot = Bot(token=self.bot_token)
        else:
            logger.warning("Telegram bot token or chat ID not configured")
    
    def send_message_sync(self, message: str, parse_mode: str = 'HTML') -> bool:
        """동기적으로 메시지 전송"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self._send_message(message, parse_mode))
        except Exception as e:
            logger.error(f"메시지 전송 오류: {e}")
            return False
    
    async def _send_message(self, message: str, parse_mode: str = 'HTML') -> bool:
        """비동기 메시지 전송"""
        if not self.bot or not self.chat_id:
            return False
        
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=parse_mode
            )
            return True
        except Exception as e:
            logger.error(f"Telegram 전송 오류: {e}")
            return False

# 전역 인스턴스
telegram_notifier = TelegramNotifier()

# 편의 함수들
def send_system_alert(alert_type: str, message: str) -> bool:
    """시스템 알림 전송"""
    emoji_map = {
        'error': '🚨',
        'warning': '⚠️', 
        'info': 'ℹ️',
        'success': '✅'
    }
    
    emoji = emoji_map.get(alert_type, 'ℹ️')
    
    formatted_message = f"""{emoji} 시스템 알림
📅 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📋 유형: {alert_type.upper()}

📝 메시지:
{message}
"""
    return telegram_notifier.send_message_sync(formatted_message)

def send_new_data_alert(new_records: List[Dict]) -> bool:
    """신규 데이터 알림 전송"""
    if not new_records:
        return True
    
    message = f"""🌰 마카다미아 무역 데이터 신규 업데이트
📅 업데이트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 신규 데이터: {len(new_records)}건
"""
    return telegram_notifier.send_message_sync(message)

def send_analysis_summary(analysis_text: str, period_days: int = 7) -> bool:
    """AI 분석 요약 전송"""
    summary = analysis_text[:300] + "..." if len(analysis_text) > 300 else analysis_text
    
    message = f"""🧠 AI 분석 요약 ({period_days}일)
📅 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}

📊 주요 인사이트:
{summary}
"""
    return telegram_notifier.send_message_sync(message)

def send_daily_summary(summary_data: Dict) -> bool:
    """일일 요약 전송"""
    message = f"""📊 마카다미아 무역 일일 요약
📅 날짜: {datetime.now().strftime('%Y년 %m월 %d일')}

🔍 데이터 수집 현황:
• 총 거래: {summary_data.get('total_records', 0)}건
• 총 거래액: ${summary_data.get('total_value', 0):,.0f}
"""
    return telegram_notifier.send_message_sync(message)
