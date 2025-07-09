import openai
from openai import OpenAI
from typing import List, Dict
import json
from datetime import datetime, timedelta
from config import Config
from models import DatabaseManager
import logging

logger = logging.getLogger(__name__)

class MacadamiaTradeAIAgent:
    def __init__(self):
        self.config = Config()
        self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
        self.db = DatabaseManager(self.config.DATABASE_URL)
    
    def analyze_trade_trends(self, days=7) -> str:
        """최근 무역 동향 분석"""
        records = self.db.get_latest_records(days)
        
        if not records:
            return "최근 마카다미아 무역 데이터가 없습니다."
        
        # 데이터 정리
        data_summary = self._prepare_data_summary(records)
        
        # AI 분석 요청
        prompt = f"""
        다음은 최근 {days}일간의 마카다미아 무역 데이터입니다:
        
        {json.dumps(data_summary, ensure_ascii=False, indent=2)}
        
        이 데이터를 바탕으로 다음 사항들을 분석해주세요:
        1. 주요 수출국과 수입국
        2. 거래량 및 거래금액 동향
        3. 주요 무역업체들
        4. 가격 트렌드
        5. 주목할만한 변화나 패턴
        
        한국어로 상세하고 전문적인 분석 보고서를 작성해주세요.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 국제무역 전문 분석가입니다. 마카다미아 무역 데이터를 분석하여 인사이트를 제공합니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI 분석 오류: {e}")
            return f"분석 중 오류가 발생했습니다: {e}"
    
    def _prepare_data_summary(self, records) -> Dict:
        """데이터베이스 레코드를 분석용 요약 데이터로 변환"""
        summary = {
            'total_records': len(records),
            'date_range': {
                'start': min(record.date for record in records).isoformat(),
                'end': max(record.date for record in records).isoformat()
            },
            'by_country': {},
            'by_company': {},
            'total_value': 0,
            'trade_types': {'export': 0, 'import': 0}
        }
        
        for record in records:
            # 국가별 집계
            country_key = f"{record.country_origin} -> {record.country_destination}"
            if country_key not in summary['by_country']:
                summary['by_country'][country_key] = {
                    'count': 0,
                    'total_value': 0,
                    'total_quantity': 0
                }
            
            summary['by_country'][country_key]['count'] += 1
            summary['by_country'][country_key]['total_value'] += record.value_usd or 0
            summary['by_country'][country_key]['total_quantity'] += record.quantity or 0
            
            # 회사별 집계
            if record.company_exporter:
                if record.company_exporter not in summary['by_company']:
                    summary['by_company'][record.company_exporter] = {
                        'type': 'exporter',
                        'total_value': 0,
                        'count': 0
                    }
                summary['by_company'][record.company_exporter]['total_value'] += record.value_usd or 0
                summary['by_company'][record.company_exporter]['count'] += 1
            
            # 전체 집계
            summary['total_value'] += record.value_usd or 0
            summary['trade_types'][record.trade_type] += 1
        
        return summary
    
    def generate_daily_report(self) -> str:
        """일일 보고서 생성 및 텔레그램 알림"""
        analysis = self.analyze_trade_trends(1)
        weekly_analysis = self.analyze_trade_trends(7)
        
        report = f"""
# 마카다미아 무역 일일 보고서
**생성일시:** {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}

## 📊 오늘의 동향
{analysis}

## 📈 주간 동향 (최근 7일)
{weekly_analysis}

---
*이 보고서는 AI 에이전트에 의해 자동 생성되었습니다.*
        """
        
        # 텔레그램으로 분석 요약 전송
        try:
            # send_analysis_summary(analysis, 1)
            logger.info("일일 분석 요약 생성 완료 (텔레그램 전송은 별도 처리)")
        except Exception as e:
            logger.error(f"분석 처리 오류: {e}")
        
        return report
    
    def analyze_with_notification(self, days: int = 7) -> str:
        """분석 수행 및 텔레그램 알림"""
        try:
            analysis = self.analyze_trade_trends(days)
            
            # 텔레그램으로 분석 결과 전송 (별도 처리)
            # send_analysis_summary(analysis, days)
            
            return analysis
            
        except Exception as e:
            # 분석 오류 알림 (별도 처리)
            # send_system_alert('error', f"AI 분석 중 오류 발생 ({days}일): {str(e)}")
            logger.error(f"AI 분석 중 오류 발생 ({days}일): {str(e)}")
            raise e
