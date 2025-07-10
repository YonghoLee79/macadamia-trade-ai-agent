"""
텔레그램 관련 API 핸들러
"""
from flask import jsonify
from datetime import datetime
import logging
from telegram_notifier import send_system_alert, send_daily_summary

logger = logging.getLogger(__name__)

class TelegramAPI:
    """텔레그램 API 핸들러"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def test_telegram(self):
        """텔레그램 연결 테스트"""
        try:
            # 테스트 메시지 전송
            success = send_system_alert(
                'info',
                '마카다미아 무역 AI 에이전트 텔레그램 연결 테스트입니다. 🌰'
            )
            
            if success:
                return jsonify({
                    'success': True,
                    'message': '텔레그램 연결 테스트 성공!'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '텔레그램 메시지 전송 실패'
                })
        except Exception as e:
            logger.error(f"Telegram test error: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    def send_manual_summary(self):
        """수동 일일 요약 전송"""
        try:
            # 요약 데이터 생성
            records = self.db_manager.get_latest_records(1)
            
            total_records = len(records)
            total_value = sum(record.value_usd or 0 for record in records)
            
            country_stats = {}
            for record in records:
                country = record.country_origin
                if country not in country_stats:
                    country_stats[country] = {'value': 0, 'count': 0}
                country_stats[country]['value'] += record.value_usd or 0
                country_stats[country]['count'] += 1
            
            top_countries = sorted(country_stats.items(), key=lambda x: x[1]['value'], reverse=True)[:5]
            
            summary_data = {
                'total_records': total_records,
                'total_value': total_value,
                'top_countries': top_countries,
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            
            # 텔레그램으로 전송
            success = send_daily_summary(summary_data)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': '일일 요약이 텔레그램으로 전송되었습니다.'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '텔레그램 전송 실패'
                })
        except Exception as e:
            logger.error(f"Manual summary error: {e}")
            return jsonify({'success': False, 'error': str(e)})
