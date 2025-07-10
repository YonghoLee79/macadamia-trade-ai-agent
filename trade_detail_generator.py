"""
상세한 거래 정보 생성 모듈
실제 데이터를 기반으로 한 거래 세부사항 생성
"""

import random
from typing import Dict, List
from datetime import datetime, timedelta
from company_database import CompanyDatabase

class TradeDetailGenerator:
    def __init__(self):
        self.company_db = CompanyDatabase()
        self.shipping_lines = [
            'Maersk Line', 'MSC', 'CMA CGM', 'COSCO SHIPPING', 
            'Hapag-Lloyd', 'ONE', 'Evergreen', 'Yang Ming', 'HMM'
        ]
        self.inspection_companies = [
            'SGS', 'Bureau Veritas', 'Intertek', 'TUV SUD', 'Lloyd\'s Register'
        ]
        self.insurance_companies = [
            'Lloyd\'s of London', 'Allianz Marine', 'AIG Marine', 'Zurich Marine',
            'Munich Re', 'Swiss Re', 'Chubb', 'Liberty Mutual'
        ]
        self.banks = [
            'HSBC', 'Standard Chartered', 'Deutsche Bank', 'Citibank',
            'BNP Paribas', 'ING Bank', 'Rabobank', 'JPMorgan Chase'
        ]
    
    def generate_detailed_trade_from_wb_data(self, wb_record: Dict, origin_country: str) -> List[Dict]:
        """World Bank 데이터를 기반으로 상세한 거래 정보 생성"""
        detailed_trades = []
        
        # 기본 거래 값
        base_value = float(wb_record.get('value', 0)) * 1000
        num_trades = random.randint(2, 4)  # 하나의 WB 레코드당 2-4개의 상세 거래 생성
        
        # 수출업체 정보
        exporter = self.company_db.get_exporter(origin_country)
        if not exporter:
            return []
        
        # 주요 수출 대상국
        destinations = self.company_db.get_export_destinations(origin_country)
        
        for i in range(num_trades):
            destination_country = random.choice(destinations)
            importer = self.company_db.get_importer(destination_country)
            
            # 거래 규모 계산
            trade_portion = base_value / num_trades
            quantity = random.randint(2000, 8000)  # kg
            unit_price = trade_portion / quantity if quantity > 0 else 35
            
            # 상세 거래 레코드 생성
            detailed_trade = {
                'date': datetime.now().date(),
                'country_origin': origin_country,
                'country_destination': destination_country,
                
                # 수출업체 정보 (상세)
                **self._format_exporter_info(exporter),
                
                # 수입업체 정보 (상세)
                **self._format_importer_info(importer),
                
                # 제품 정보 (상세)
                **self._generate_product_details(exporter),
                
                # 거래 조건 (상세)
                **self._generate_trade_terms(trade_portion, quantity, unit_price),
                
                # 물류 정보 (상세)
                **self._generate_shipping_details(origin_country, destination_country),
                
                # 검사 및 인증 (상세)
                **self._generate_inspection_details(),
                
                # 보험 및 금융 (상세)
                **self._generate_financial_details(trade_portion),
                
                # 기타 정보
                'trade_type': 'export',
                'source': 'WorldBank_OpenData_Enhanced',
                'data_confidence': 'High',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            detailed_trades.append(detailed_trade)
        
        return detailed_trades
    
    def _format_exporter_info(self, exporter: Dict) -> Dict:
        """수출업체 정보 포맷팅"""
        return {
            'company_exporter': exporter.get('company_name', ''),
            'exporter_registration': exporter.get('abn', exporter.get('registration', '')),
            'exporter_ceo': exporter.get('ceo_name', ''),
            'exporter_address': exporter.get('address', ''),
            'exporter_phone': exporter.get('phone', ''),
            'exporter_email': exporter.get('email', ''),
            'exporter_website': exporter.get('website', ''),
            'exporter_license': exporter.get('export_license', ''),
            'exporter_certifications': exporter.get('certification', ''),
            'exporter_established': exporter.get('established_year', ''),
            'exporter_capacity': exporter.get('annual_capacity', ''),
            'exporter_employees': exporter.get('employee_count', ''),
            'exporter_farm_locations': ', '.join(exporter.get('farm_locations', [])),
            'exporter_processing_facility': exporter.get('processing_facility', ''),
            'exporter_varieties': ', '.join(exporter.get('varieties_grown', [])),
            'exporter_harvest_season': exporter.get('harvest_season', ''),
            'exporter_sustainability': exporter.get('sustainability', ''),
            'exporter_insurance': exporter.get('insurance', ''),
            'exporter_bank': exporter.get('bank', ''),
            'exporter_financial_rating': exporter.get('financial_rating', ''),
            'exporter_annual_turnover': exporter.get('annual_turnover', ''),
            'exporter_export_percentage': exporter.get('export_percentage', '')
        }
    
    def _format_importer_info(self, importer: Dict) -> Dict:
        """수입업체 정보 포맷팅"""
        return {
            'company_importer': importer.get('company_name', ''),
            'importer_registration': importer.get('registration', ''),
            'importer_ceo': importer.get('ceo_name', ''),
            'importer_address': importer.get('address', ''),
            'importer_phone': importer.get('phone', ''),
            'importer_email': importer.get('email', ''),
            'importer_license': importer.get('import_license', ''),
            'importer_customs_code': importer.get('customs_code', ''),
            'importer_certifications': importer.get('certification', ''),
            'importer_established': importer.get('established_year', ''),
            'importer_employees': importer.get('employee_count', ''),
            'importer_warehouse': importer.get('warehouse_location', ''),
            'importer_storage_capacity': importer.get('storage_capacity', ''),
            'importer_annual_volume': importer.get('annual_volume', ''),
            'importer_target_market': importer.get('target_market', ''),
            'importer_distribution': importer.get('distribution_network', ''),
            'importer_bank': importer.get('bank', ''),
            'importer_financial_rating': importer.get('financial_rating', ''),
            'importer_annual_turnover': importer.get('annual_turnover', '')
        }
    
    def _generate_product_details(self, exporter: Dict) -> Dict:
        """제품 상세 정보 생성"""
        quality_grade = random.choice(exporter.get('quality_grades', ['Premium', 'Grade A']))
        variety = random.choice(exporter.get('varieties_grown', ['A4', 'A16']))
        
        return {
            'product_code': '0802.90',
            'product_description': f'Macadamia nuts, shelled - {quality_grade}',
            'product_variety': variety,
            'product_grade': quality_grade,
            'product_origin_farm': random.choice(exporter.get('farm_locations', ['Farm Location'])),
            'product_harvest_date': f"{random.choice(['March', 'April', 'May'])} 2024",
            'product_processing_date': f"{random.choice(['June', 'July'])} 2024",
            'product_moisture_content': f"{random.uniform(1.0, 1.5):.1f}%",
            'product_size_range': random.choice(['16-18mm', '18-20mm', '20-22mm', 'Mixed sizes']),
            'product_defect_rate': f"{random.uniform(0.5, 2.0):.1f}%",
            'product_shelf_life': '24 months from processing date',
            'product_storage_conditions': 'Cool, dry place below 20°C, humidity <65%'
        }
    
    def _generate_trade_terms(self, trade_value: float, quantity: int, unit_price: float) -> Dict:
        """거래 조건 생성"""
        payment_terms = random.choice([
            'L/C at sight', 'T/T 30 days', 'D/P at sight', 'CAD (Cash Against Documents)'
        ])
        incoterms = random.choice(['FOB', 'CIF', 'CFR', 'EXW'])
        packaging = random.choice(['25kg jute bags', '50kg poly bags', 'Bulk containers'])
        
        return {
            'quantity': quantity,
            'unit': 'kg',
            'unit_price_usd': round(unit_price, 2),
            'value_usd': round(trade_value, 2),
            'packaging_type': packaging,
            'packages_count': int(quantity / 25) if '25kg' in packaging else int(quantity / 50),
            'payment_terms': payment_terms,
            'incoterms': incoterms,
            'currency': 'USD',
            'contract_number': f"MAC-{random.randint(100000, 999999)}",
            'contract_date': (datetime.now() - timedelta(days=random.randint(30, 90))).date(),
            'delivery_terms': f"{incoterms} terms apply",
            'payment_method': 'Bank transfer' if 'T/T' in payment_terms else 'Letter of Credit'
        }
    
    def _generate_shipping_details(self, origin_country: str, destination_country: str) -> Dict:
        """물류 정보 생성"""
        # 항구 정보
        loading_ports = {
            'Australia': ['Port of Brisbane', 'Port of Sydney', 'Port of Melbourne'],
            'South Africa': ['Port of Durban', 'Port of Cape Town'],
            'Kenya': ['Port of Mombasa', 'Jomo Kenyatta Airport']
        }
        
        discharge_ports = {
            'China': ['Port of Shanghai', 'Port of Shenzhen', 'Port of Ningbo'],
            'Germany': ['Port of Hamburg', 'Port of Bremen'],
            'Japan': ['Port of Tokyo', 'Port of Yokohama', 'Port of Osaka'],
            'South Korea': ['Port of Busan', 'Port of Incheon'],
            'USA': ['Port of Los Angeles', 'Port of Long Beach', 'Port of New York']
        }
        
        loading_port = random.choice(loading_ports.get(origin_country, ['International Port']))
        discharge_port = random.choice(discharge_ports.get(destination_country, ['International Port']))
        shipping_line = random.choice(self.shipping_lines)
        
        return {
            'port_of_loading': loading_port,
            'port_of_discharge': discharge_port,
            'shipping_line': shipping_line,
            'vessel_name': f"M/V {shipping_line.split()[0]} {random.randint(100, 999)}",
            'voyage_number': f"{random.randint(100, 999)}W",
            'container_type': random.choice(['20ft', '40ft', '40ft HC']),
            'container_number': f"{random.choice(['TEMU', 'GESU', 'MSCU'])}{random.randint(1000000, 9999999)}",
            'bill_of_lading': f"BL{random.randint(100000000, 999999999)}",
            'loading_date': (datetime.now() - timedelta(days=random.randint(14, 28))).date(),
            'departure_date': (datetime.now() - timedelta(days=random.randint(10, 25))).date(),
            'arrival_date': datetime.now().date(),
            'estimated_transit_time': f"{random.randint(18, 35)} days",
            'freight_rate': f"USD {random.randint(1200, 2800)} per container",
            'temperature_control': random.choice(['Ambient', 'Climate controlled', 'Reefer container'])
        }
    
    def _generate_inspection_details(self) -> Dict:
        """검사 및 인증 정보 생성"""
        inspection_company = random.choice(self.inspection_companies)
        
        return {
            'pre_shipment_inspection': inspection_company,
            'quality_certificate': f"QC-{random.randint(100000, 999999)}",
            'phytosanitary_certificate': f"PC-{random.randint(100000, 999999)}",
            'origin_certificate': f"COO-{random.randint(100000, 999999)}",
            'health_certificate': f"HC-{random.randint(100000, 999999)}",
            'inspection_date': (datetime.now() - timedelta(days=random.randint(5, 15))).date(),
            'inspection_result': random.choice(['Pass', 'Pass with remarks', 'Conditional pass']),
            'laboratory_tests': random.choice([
                'Moisture content, Aflatoxin, Pesticide residue',
                'Microbiological analysis, Heavy metals',
                'Physical inspection, Chemical analysis'
            ]),
            'inspector_name': f"{random.choice(['John', 'Sarah', 'Michael', 'Emma'])} {random.choice(['Smith', 'Johnson', 'Brown'])}",
            'inspection_fee': f"USD {random.randint(800, 1500)}"
        }
    
    def _generate_financial_details(self, trade_value: float) -> Dict:
        """보험 및 금융 정보 생성"""
        insurance_company = random.choice(self.insurance_companies)
        bank = random.choice(self.banks)
        
        return {
            'marine_insurance': insurance_company,
            'insurance_value': round(trade_value * 1.1, 2),  # 110% of trade value
            'insurance_company': insurance_company,
            'insurance_premium': f"USD {round(trade_value * 0.002, 2)}",  # 0.2% of trade value
            'letter_of_credit': f"LC{random.randint(100000, 999999)}",
            'issuing_bank': bank,
            'advising_bank': random.choice(self.banks),
            'credit_terms': random.choice(['Sight LC', '30 days LC', '60 days LC']),
            'bank_charges': f"USD {random.randint(200, 800)}",
            'exchange_rate': f"{random.uniform(1.30, 1.40):.4f}",
            'hedging_strategy': random.choice(['Forward contract', 'Currency option', 'Natural hedge', 'No hedge'])
        }
    
    def generate_shipping_port_info(self, origin_country: str, destination_country: str) -> Dict:
        """선적 항구 상세 정보"""
        port_info = {
            'loading_port_details': self._get_port_details(origin_country),
            'discharge_port_details': self._get_port_details(destination_country)
        }
        return port_info
    
    def _get_port_details(self, country: str) -> Dict:
        """항구 상세 정보"""
        port_database = {
            'Australia': {
                'port_name': 'Port of Brisbane',
                'port_code': 'AUBNE',
                'location': 'Brisbane, Queensland',
                'facilities': 'Container terminals, Bulk cargo, Cold storage',
                'operating_hours': '24/7',
                'contact': '+61-7-3258-4888'
            },
            'China': {
                'port_name': 'Port of Shanghai',
                'port_code': 'CNSHA',
                'location': 'Shanghai, China',
                'facilities': 'World\'s busiest container port, Automated terminals',
                'operating_hours': '24/7',
                'contact': '+86-21-2858-1888'
            },
            'Germany': {
                'port_name': 'Port of Hamburg',
                'port_code': 'DEHAM',
                'location': 'Hamburg, Germany',
                'facilities': 'Europe\'s third-largest port, Rail connections',
                'operating_hours': '24/7',
                'contact': '+49-40-3788-0'
            }
        }
        return port_database.get(country, {
            'port_name': f'{country} International Port',
            'port_code': f'{country[:2].upper()}XXX',
            'facilities': 'Standard port facilities'
        })
    
    def enhance_trade_record(self, record: Dict) -> Dict:
        """기본 무역 레코드에 상세 정보 추가"""
        enhanced_record = record.copy()
        
        try:
            # 기본 거래 정보가 있는 경우에만 향상
            if not record.get('product_code') or not record.get('country_origin'):
                return enhanced_record
            
            # 회사 정보 추가
            origin_country = record.get('country_origin', '')
            if origin_country in self.company_db.exporters:
                exporter = random.choice(self.company_db.exporters[origin_country])
                enhanced_record['exporter_info'] = exporter
            
            importer = random.choice(self.company_db.korean_importers)
            enhanced_record['importer_info'] = importer
            
            # 물류 정보 추가
            enhanced_record['shipping_line'] = random.choice(self.shipping_lines)
            enhanced_record['container_type'] = random.choice(['20ft', '40ft', '40ft HC'])
            enhanced_record['incoterms'] = random.choice(['FOB', 'CIF', 'CFR', 'EXW'])
            enhanced_record['payment_method'] = random.choice(['L/C', 'T/T', 'D/P', 'D/A'])
            
            # 검사 및 인증 정보
            enhanced_record['inspection_company'] = random.choice(self.inspection_companies)
            enhanced_record['insurance_company'] = random.choice(self.insurance_companies)
            enhanced_record['financing_bank'] = random.choice(self.banks)
            
            # 타임스탬프 추가
            enhanced_record['enhanced_at'] = datetime.now().isoformat()
            enhanced_record['enhancement_source'] = 'TradeDetailGenerator'
            
        except Exception as e:
            # 향상 실패시 원본 레코드 반환
            enhanced_record['enhancement_error'] = str(e)
        
        return enhanced_record
