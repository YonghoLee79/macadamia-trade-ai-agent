#!/usr/bin/env python3
"""
상세 시뮬레이션 데이터 생성 및 테스트
"""

from data_scraper import MacadamiaTradeDataScraper
from models import DatabaseManager
import os

def test_detailed_simulation():
    print("=== 상세 시뮬레이션 데이터 생성 테스트 ===")
    
    # 기존 데이터베이스 삭제하고 새로 시작
    if os.path.exists('macadamia_trade.db'):
        os.remove('macadamia_trade.db')
        print("기존 데이터베이스 삭제 완료")
    
    # 새로운 시뮬레이션 데이터 생성
    scraper = MacadamiaTradeDataScraper()
    simulation_data = scraper.generate_simulation_data()
    
    print(f"생성된 시뮬레이션 데이터: {len(simulation_data)}건")
    
    # 첫 번째 레코드의 상세 정보 출력
    if simulation_data:
        print("\n=== 샘플 레코드 (첫 번째) ===")
        sample = simulation_data[0]
        
        # 기본 정보
        print("\n[ 기본 거래 정보 ]")
        print(f"신고번호: {sample.get('declaration_number')}")
        print(f"거래일자: {sample.get('date')}")
        print(f"원산지: {sample.get('country_origin')}")
        
        # 수입업체 정보
        print("\n[ 수입업체 정보 ]")
        print(f"업체명: {sample.get('company_importer')}")
        print(f"사업자번호: {sample.get('importer_business_number')}")
        print(f"대표자: {sample.get('importer_ceo')}")
        print(f"주소: {sample.get('importer_address')}")
        print(f"전화: {sample.get('importer_phone')}")
        print(f"업종: {sample.get('importer_business_type')}")
        print(f"설립연도: {sample.get('importer_established')}")
        print(f"직원수: {sample.get('importer_employees')}")
        
        # 수출업체 정보
        print("\n[ 수출업체 정보 ]")
        print(f"업체명: {sample.get('company_exporter')}")
        print(f"사업자번호: {sample.get('exporter_business_number')}")
        print(f"대표자: {sample.get('exporter_ceo')}")
        print(f"주소: {sample.get('exporter_address')}")
        print(f"인증: {sample.get('exporter_certification')}")
        print(f"농장위치: {sample.get('exporter_farm_location')}")
        print(f"가공능력: {sample.get('exporter_capacity')}")
        
        # 품목 정보
        print("\n[ 품목 정보 ]")
        print(f"HS 코드: {sample.get('product_code')}")
        print(f"품목명: {sample.get('product_description')}")
        print(f"상세품목명: {sample.get('product_detailed_description')}")
        print(f"품질등급: {sample.get('quality_grade')}")
        print(f"수량: {sample.get('quantity')} {sample.get('unit')}")
        print(f"단가: ${sample.get('unit_price_usd')}")
        print(f"총액: ${sample.get('value_usd')}")
        
        # 세금 정보
        print("\n[ 세금 및 비용 ]")
        print(f"적용 관세율: {sample.get('tariff_rate_applied')}")
        print(f"관세액: ${sample.get('tariff_amount')}")
        print(f"부가세: ${sample.get('vat_amount')}")
        print(f"통관수수료: ${sample.get('customs_fee')}")
        print(f"검사수수료: ${sample.get('inspection_fee')}")
        print(f"환율: {sample.get('exchange_rate')} KRW/USD")
        print(f"총 비용: {sample.get('total_cost_krw')} 원")
        
        # 물류 정보
        print("\n[ 물류 정보 ]")
        print(f"선적항: {sample.get('port_of_loading')}")
        print(f"도착항: {sample.get('port_of_discharge')}")
        print(f"선박명: {sample.get('vessel_name')}")
        print(f"항해번호: {sample.get('voyage_number')}")
        print(f"컨테이너: {sample.get('container_type')} ({sample.get('container_number')})")
        print(f"온도관리: {sample.get('temperature_control')}")
        
        # 통관 정보
        print("\n[ 통관 정보 ]")
        print(f"통관업체: {sample.get('customs_broker_company')}")
        print(f"담당자: {sample.get('customs_broker_rep')}")
        print(f"검사기관: {', '.join(sample.get('inspection_agencies', []))}")
        print(f"품질검사: {sample.get('quality_inspection')}")
        print(f"검역상태: {sample.get('quarantine_status')}")
        
        # 특이사항
        print("\n[ 특이사항 ]")
        print(f"{sample.get('special_notes')}")
        
        # 데이터베이스 저장 테스트
        print("\n=== 데이터베이스 저장 테스트 ===")
        db = DatabaseManager('sqlite:///macadamia_trade.db')
        
        saved_count = 0
        for data in simulation_data[:3]:  # 처음 3건만 저장 테스트
            try:
                record = db.save_record(data)
                saved_count += 1
                print(f"레코드 {record.id} 저장 완료")
            except Exception as e:
                print(f"저장 오류: {e}")
        
        print(f"총 {saved_count}건 저장 완료")
        
        # 저장된 상세 데이터 조회 테스트
        if saved_count > 0:
            print("\n=== 저장된 상세 데이터 조회 테스트 ===")
            detailed_record = db.get_detailed_record(1)
            if detailed_record:
                print("첫 번째 레코드의 상세 정보:")
                for key, value in detailed_record.items():
                    if key not in ['id', 'created_at']:  # 기본 필드 제외
                        print(f"  {key}: {value}")
        
        db.close()

if __name__ == "__main__":
    test_detailed_simulation()
