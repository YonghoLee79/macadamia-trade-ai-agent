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
    
    async def send_message(self, message: str, parse_mode: str = 'HTML') -> bool:
        """텔레그램으로 메시지 전송"""
        if not self.bot or not self.chat_id:
            logger.warning("Telegram not configured, skipping message")
            return False
        
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=parse_mode
            )
            logger.info("Telegram message sent successfully")
            return True
        except TelegramError as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Telegram message: {e}")
            return False
    
    def send_message_sync(self, message: str, parse_mode: str = 'HTML') -> bool:
        """동기적으로 메시지 전송 (비동기 이벤트 루프가 없는 환경용)"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.send_message(message, parse_mode))
    
    def format_new_data_alert(self, new_records: List[Dict]) -> str:
        """신규 데이터 알림 메시지 포맷"""
        if not new_records:
            return ""
        
        message = f"""🌰 <b>마카다미아 무역 데이터 신규 업데이트</b>
📅 <b>업데이트 시간:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 <b>신규 데이터:</b> {len(new_records)}건

<b>📈 주요 신규 거래:</b>
"""
        
        # 상위 5개 거래만 표시
        top_records = sorted(new_records, key=lambda x: x.get('value_usd', 0), reverse=True)[:5]
        
        for i, record in enumerate(top_records, 1):
            country_from = record.get('country_origin', 'Unknown')
            country_to = record.get('country_destination', 'Unknown')
            value = record.get('value_usd', 0)
            quantity = record.get('quantity', 0)
            
            message += f"""
{i}. 🌍 <b>{country_from}</b> → <b>{country_to}</b>
   💰 ${value:,.0f} | 📦 {quantity:,.0f}kg
"""
        
        if len(new_records) > 5:
            message += f"\n📋 <i>그 외 {len(new_records) - 5}건의 거래가 더 있습니다.</i>"
        
        message += f"\n\n🔗 <a href='http://localhost:5000'>대시보드에서 자세히 보기</a>"
        
        return message
    
    def format_analysis_summary(self, analysis_text: str, period_days: int) -> str:
        """AI 분석 요약 메시지 포맷"""
        # 분석 텍스트를 요약 (첫 3줄만 사용)
        lines = analysis_text.split('\n')
        summary_lines = [line.strip() for line in lines[:3] if line.strip()]
        summary = '\n'.join(summary_lines)
        
        if len(summary) > 200:
            summary = summary[:200] + "..."
        
        message = f"""🧠 <b>AI 분석 요약 ({period_days}일)</b>
📅 <b>분석 시간:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}

📊 <b>주요 인사이트:</b>
{summary}

🔗 <a href='http://localhost:5000'>전체 분석 보기</a>
"""
        return message
    
    def format_system_alert(self, alert_type: str, message: str) -> str:
        """시스템 알림 메시지 포맷"""
        emoji_map = {
            'error': '🚨',
            'warning': '⚠️',
            'info': 'ℹ️',
            'success': '✅'
        }
        
        emoji = emoji_map.get(alert_type, 'ℹ️')
        
        formatted_message = f"""{emoji} <b>시스템 알림</b>
📅 <b>시간:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📋 <b>유형:</b> {alert_type.upper()}

📝 <b>메시지:</b>
{message}
"""
        return formatted_message
    
    def format_daily_summary(self, summary_data: Dict) -> str:
        """일일 요약 메시지 포맷"""
        total_records = summary_data.get('total_records', 0)
        total_value = summary_data.get('total_value', 0)
        top_countries = summary_data.get('top_countries', [])
        
        message = f"""📊 <b>마카다미아 무역 일일 요약</b>
📅 <b>날짜:</b> {datetime.now().strftime('%Y년 %m월 %d일')}

📈 <b>오늘의 통계:</b>
• 거래 건수: {total_records:,}건
• 총 거래액: ${total_value:,.0f}
"""
        
        if top_countries:
            message += "\n🌍 <b>주요 거래국:</b>\n"
            for i, (country, data) in enumerate(top_countries[:3], 1):
                message += f"  {i}. {country}: ${data.get('value', 0):,.0f}\n"
        
        message += f"\n🔗 <a href='http://localhost:5000'>상세 대시보드 보기</a>"
        
        return message

# 전역 인스턴스
telegram_notifier = TelegramNotifier()

# 편의 함수들
def send_new_data_alert(new_records: List[Dict]) -> bool:
    """신규 데이터 알림 전송"""
    if not new_records:
        return True
    
    message = telegram_notifier.format_new_data_alert(new_records)
    if message:
        return telegram_notifier.send_message_sync(message)
    return True

def send_analysis_summary(analysis_text: str, period_days: int = 7) -> bool:
    """AI 분석 요약 전송"""
    message = telegram_notifier.format_analysis_summary(analysis_text, period_days)
    return telegram_notifier.send_message_sync(message)

def send_system_alert(alert_type: str, message: str) -> bool:
    """시스템 알림 전송"""
    formatted_message = telegram_notifier.format_system_alert(alert_type, message)
    return telegram_notifier.send_message_sync(formatted_message)

def send_daily_summary(summary_data: Dict) -> bool:
    """일일 요약 전송"""
    message = telegram_notifier.format_daily_summary(summary_data)
    return telegram_notifier.send_message_sync(message)
