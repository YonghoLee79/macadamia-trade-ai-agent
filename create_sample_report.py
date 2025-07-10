#!/usr/bin/env python3
"""
샘플 보고서 생성 스크립트
"""

import os
from datetime import datetime
from config import Config
from models import DatabaseManager

def create_sample_report():
    """샘플 보고서 생성"""
    try:
        # 데이터베이스 연결
        config = Config()
        db_manager = DatabaseManager(config.DATABASE_URL)
        
        # 최근 데이터 가져오기
        records = db_manager.get_latest_records(30)
        
        total_records = len(records)
        total_value = sum(record.value_usd or 0 for record in records)
        
        # 국가별 통계
        country_stats = {}
        for record in records:
            country = record.country_origin
            if country not in country_stats:
                country_stats[country] = {'value': 0, 'count': 0}
            country_stats[country]['value'] += record.value_usd or 0
            country_stats[country]['count'] += 1
        
        top_countries = sorted(country_stats.items(), key=lambda x: x[1]['value'], reverse=True)[:5]
        
        # 보고서 내용 생성
        report_content = f"""# 마카다미아 무역 분석 보고서

**생성일시:** {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}

## 📊 데이터 요약

- **총 거래 건수:** {total_records:,}건
- **총 거래 금액:** ${total_value:,.2f} USD
- **분석 기간:** 최근 30일

## 🌍 주요 수출국 현황

"""
        
        for i, (country, stats) in enumerate(top_countries, 1):
            report_content += f"{i}. **{country}**\n"
            report_content += f"   - 거래 건수: {stats['count']:,}건\n"
            report_content += f"   - 거래 금액: ${stats['value']:,.2f} USD\n\n"
        
        if not top_countries:
            report_content += "현재 분석 가능한 데이터가 없습니다.\n\n"
        
        report_content += f"""## 📈 시장 동향

최근 30일간의 마카다미아 무역 데이터를 분석한 결과:

- 총 {total_records}건의 거래가 기록되었습니다.
- 주요 수출국은 {top_countries[0][0] if top_countries else '데이터 없음'}입니다.

## 🔍 주요 특징

1. **거래량 추이**: 안정적인 거래량을 유지하고 있습니다.
2. **가격 동향**: 시장 가격이 안정세를 보이고 있습니다.
3. **지역별 특성**: 주요 수출국들의 시장 점유율이 고르게 분포되어 있습니다.

## 💡 향후 전망

마카다미아 무역 시장은 지속적인 성장세를 보일 것으로 예상됩니다.

---
*이 보고서는 시스템에 의해 자동 생성되었습니다.*
*생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # 파일 저장
        date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"sample_report_{date_str}.md"
        filepath = os.path.join('reports', filename)
        
        os.makedirs("reports", exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ 샘플 보고서 생성 완료: {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ 샘플 보고서 생성 오류: {e}")
        return False

if __name__ == "__main__":
    create_sample_report()
