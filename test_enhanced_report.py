#!/usr/bin/env python3
"""
개선된 리포트 생성 테스트 - 상세 시뮬레이션 데이터 활용
"""

from excel_reporter import ExcelReporter
from models import DatabaseManager
from datetime import datetime, timedelta

def test_enhanced_report():
    print("=== 개선된 리포트 생성 테스트 ===")
    
    # 데이터베이스에서 최근 데이터 조회
    db = DatabaseManager('sqlite:///macadamia_trade.db')
    
    # 최근 데이터 조회
    recent_records = db.get_recent_records(limit=10)
    
    if not recent_records:
        print("데이터가 없습니다. 먼저 시뮬레이션 데이터를 생성하세요.")
        return
    
    print(f"데이터베이스에서 {len(recent_records)}건의 레코드 조회")
    
    # 상세 데이터로 변환
    detailed_data = []
    for record in recent_records:
        detailed_record = db.get_detailed_record(record.id)
        if detailed_record:
            detailed_data.append(detailed_record)
    
    print(f"상세 데이터 {len(detailed_data)}건 준비 완료")
    
    # 리포트 생성
    reporter = ExcelReporter()
    
    # 날짜 범위 설정 (최근 30일)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    report_filename = f"enhanced_macadamia_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    try:
        # 상세 데이터를 사용하여 리포트 생성
        report_content = reporter.create_enhanced_report(
            detailed_data, 
            start_date, 
            end_date,
            include_detailed_analysis=True
        )
        
        # 리포트 파일 저장
        report_path = f"reports/{report_filename}"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"리포트 생성 완료: {report_path}")
        
        # 리포트 내용 미리보기
        print("\n=== 리포트 내용 미리보기 ===")
        lines = report_content.split('\n')
        for line in lines[:30]:  # 처음 30줄만 출력
            print(line)
        
        if len(lines) > 30:
            print(f"\n... (총 {len(lines)}줄 중 30줄만 표시)")
        
    except Exception as e:
        print(f"리포트 생성 중 오류: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

if __name__ == "__main__":
    test_enhanced_report()
