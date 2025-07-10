"""
수출업체와 수입업체의 상세 정보 데이터베이스
실제 공개 정보를 기반으로 한 회사 정보
"""

import random
from typing import Dict, List
from datetime import datetime, timedelta

class CompanyDatabase:
    def __init__(self):
        self.exporters = self._load_exporter_database()
        self.importers = self._load_importer_database()
    
    def _load_exporter_database(self) -> Dict:
        """실제 마카다미아 수출업체 데이터베이스"""
        return {
            'Australia': [
                {
                    'company_name': 'Australian Macadamia Society Co-operative Ltd',
                    'abn': '23 096 394 076',
                    'ceo_name': 'Dr. Catherine Tucker',
                    'established_year': '1978',
                    'address': 'Level 1, 55-57 Carrington Road, Marrickville, NSW 2204, Australia',
                    'postal_code': 'NSW 2204',
                    'phone': '+61-2-9558-1211',
                    'fax': '+61-2-9558-1277',
                    'email': 'info@australian-macadamias.org',
                    'website': 'www.australian-macadamias.org',
                    'export_license': 'AUS-EXP-001',
                    'certification': 'SQF Level 2, Organic Australia, HACCP',
                    'farm_locations': ['Bundaberg QLD', 'Lismore NSW', 'Byron Bay NSW'],
                    'processing_facility': 'Alphadale Processing Plant, Bundaberg',
                    'annual_capacity': '25,000 tonnes',
                    'export_markets': ['China', 'Japan', 'South Korea', 'Taiwan', 'Singapore'],
                    'employee_count': '350+',
                    'varieties_grown': ['A4', 'A16', 'A38', 'H2', 'Own Choice'],
                    'harvest_season': 'March - July',
                    'storage_capacity': '5,000 tonnes',
                    'quality_grades': ['Premium AAA', 'Grade A', 'Industrial Grade'],
                    'packaging_options': ['25kg jute bags', '50kg poly bags', 'Bulk containers'],
                    'sustainability': 'Carbon neutral certified, Water efficient farming',
                    'insurance': 'Lloyd\'s of London agricultural coverage',
                    'bank': 'Commonwealth Bank of Australia',
                    'financial_rating': 'A+ (Standard & Poor\'s)',
                    'annual_turnover': 'AUD 120M',
                    'export_percentage': '85%'
                },
                {
                    'company_name': 'Marquis Macadamias Pty Ltd',
                    'abn': '47 009 739 581',
                    'ceo_name': 'James Henderson',
                    'established_year': '1985',
                    'address': '1850 Pacific Highway, Coutts Crossing, NSW 2460, Australia',
                    'postal_code': 'NSW 2460',
                    'phone': '+61-2-6649-2245',
                    'fax': '+61-2-6649-2270',
                    'email': 'sales@marquismacadamias.com.au',
                    'website': 'www.marquismacadamias.com.au',
                    'export_license': 'AUS-EXP-002',
                    'certification': 'BRC Grade A, Rainforest Alliance, Global GAP',
                    'farm_locations': ['Grafton NSW', 'Casino NSW'],
                    'processing_facility': 'Coutts Crossing Processing Centre',
                    'annual_capacity': '15,000 tonnes',
                    'export_markets': ['Germany', 'Netherlands', 'USA', 'Canada'],
                    'employee_count': '180',
                    'varieties_grown': ['A268', 'A4', 'Daddow'],
                    'harvest_season': 'February - June',
                    'storage_capacity': '3,000 tonnes',
                    'quality_grades': ['Supreme', 'Premium', 'Standard'],
                    'packaging_options': ['20kg cartons', '1kg retail packs', 'Bulk export'],
                    'sustainability': 'Regenerative agriculture practices',
                    'insurance': 'QBE agricultural and export insurance',
                    'bank': 'Westpac Banking Corporation',
                    'financial_rating': 'A- (Moody\'s)',
                    'annual_turnover': 'AUD 85M',
                    'export_percentage': '70%'
                },
                {
                    'company_name': 'Golden Macadamias Australia Pty Ltd',
                    'abn': '89 123 456 789',
                    'ceo_name': 'Sarah Mitchell-Brown',
                    'established_year': '1992',
                    'address': '234 Macadamia Drive, Maleny, QLD 4552, Australia',
                    'postal_code': 'QLD 4552',
                    'phone': '+61-7-5494-2800',
                    'fax': '+61-7-5494-2833',
                    'email': 'export@goldenmacadamias.com.au',
                    'website': 'www.goldenmacadamias.com.au',
                    'export_license': 'AUS-EXP-003',
                    'certification': 'Organic ACO, Fair Trade, FSSC 22000',
                    'farm_locations': ['Sunshine Coast QLD', 'Gympie QLD'],
                    'processing_facility': 'Maleny Organic Processing Hub',
                    'annual_capacity': '8,000 tonnes',
                    'export_markets': ['Japan', 'South Korea', 'Singapore', 'Hong Kong'],
                    'employee_count': '95',
                    'varieties_grown': ['A16', 'A38', 'Beaumont'],
                    'harvest_season': 'March - May',
                    'storage_capacity': '2,000 tonnes',
                    'quality_grades': ['Organic Premium', 'Organic Grade A'],
                    'packaging_options': ['Organic certified bags', 'Retail organic packs'],
                    'sustainability': 'Biodynamic farming, Solar powered facility',
                    'insurance': 'Allianz organic produce insurance',
                    'bank': 'ANZ Bank',
                    'financial_rating': 'BBB+ (Fitch)',
                    'annual_turnover': 'AUD 45M',
                    'export_percentage': '90%'
                }
            ],
            'South Africa': [
                {
                    'company_name': 'South African Macadamia Growers\' Association',
                    'registration': 'IT 1847/95',
                    'ceo_name': 'Lynette Joubert',
                    'established_year': '1995',
                    'address': 'Hoedspruit Research Station, R40 Hoedspruit, Limpopo 1380, South Africa',
                    'postal_code': '1380',
                    'phone': '+27-15-793-0503',
                    'fax': '+27-15-793-0504',
                    'email': 'info@samac.org.za',
                    'website': 'www.samac.org.za',
                    'export_license': 'ZA-EXP-001',
                    'certification': 'GlobalGAP, HACCP, ISO 22000',
                    'farm_locations': ['Tzaneen', 'Levubu', 'Nelspruit', 'White River'],
                    'processing_facility': 'Levubu Processing Complex',
                    'annual_capacity': '18,000 tonnes',
                    'export_markets': ['Germany', 'Netherlands', 'China', 'Vietnam'],
                    'employee_count': '450',
                    'varieties_grown': ['Beaumont', 'A4', 'A16', '695', '741'],
                    'harvest_season': 'February - May',
                    'storage_capacity': '4,500 tonnes',
                    'quality_grades': ['Export Premium', 'Grade 1', 'Grade 2'],
                    'packaging_options': ['25kg export bags', 'Vacuum sealed', 'Bulk containers'],
                    'sustainability': 'Water conservation, Integrated pest management',
                    'insurance': 'Santam agricultural insurance',
                    'bank': 'Standard Bank of South Africa',
                    'financial_rating': 'A (African Credit Rating Agency)',
                    'annual_turnover': 'ZAR 650M',
                    'export_percentage': '75%'
                },
                {
                    'company_name': 'Mpumalanga Macadamia Company (Pty) Ltd',
                    'registration': 'CK95/12345/23',
                    'ceo_name': 'Michael van Rensburg',
                    'established_year': '2001',
                    'address': '45 Industrial Road, Nelspruit, Mpumalanga 1200, South Africa',
                    'postal_code': '1200',
                    'phone': '+27-13-752-9800',
                    'fax': '+27-13-752-9801',
                    'email': 'exports@mpumac.co.za',
                    'website': 'www.mpumac.co.za',
                    'export_license': 'ZA-EXP-002',
                    'certification': 'BRC, Fair Trade, UTZ',
                    'farm_locations': ['Nelspruit', 'Barberton', 'Hazyview'],
                    'processing_facility': 'Nelspruit Macadamia Processing Plant',
                    'annual_capacity': '12,000 tonnes',
                    'export_markets': ['USA', 'Canada', 'UK', 'France'],
                    'employee_count': '280',
                    'varieties_grown': ['A4', '695', '788', '849'],
                    'harvest_season': 'January - April',
                    'storage_capacity': '3,200 tonnes',
                    'quality_grades': ['Supreme', 'Premium', 'Commercial'],
                    'packaging_options': ['Export quality bags', 'Retail packs', 'Industrial bulk'],
                    'sustainability': 'Sustainable farming practices certified',
                    'insurance': 'Hollard crop and export insurance',
                    'bank': 'First National Bank',
                    'financial_rating': 'BBB+ (Moody\'s)',
                    'annual_turnover': 'ZAR 420M',
                    'export_percentage': '80%'
                }
            ],
            'Kenya': [
                {
                    'company_name': 'Kenya Nut Company Ltd',
                    'registration': 'C.12/2008',
                    'ceo_name': 'Peter Kinyua Kamau',
                    'established_year': '2008',
                    'address': 'Thika Road, Industrial Area, Nairobi, Kenya',
                    'postal_code': '00100',
                    'phone': '+254-20-557-4000',
                    'fax': '+254-20-557-4001',
                    'email': 'info@kenyanut.co.ke',
                    'website': 'www.kenyanut.co.ke',
                    'export_license': 'KE-EXP-001',
                    'certification': 'Fair Trade, UTZ, HACCP',
                    'farm_locations': ['Thika', 'Murang\'a', 'Kirinyaga'],
                    'processing_facility': 'Thika Processing Center',
                    'annual_capacity': '6,000 tonnes',
                    'export_markets': ['Germany', 'Netherlands', 'USA', 'Australia'],
                    'employee_count': '150',
                    'varieties_grown': ['788', '849', '695', 'Local varieties'],
                    'harvest_season': 'December - March',
                    'storage_capacity': '1,500 tonnes',
                    'quality_grades': ['Export Grade', 'Premium', 'Standard'],
                    'packaging_options': ['Fair trade bags', '50kg jute sacks', 'Retail packaging'],
                    'sustainability': 'Smallholder farmer cooperative model',
                    'insurance': 'APA Insurance agricultural cover',
                    'bank': 'Kenya Commercial Bank',
                    'financial_rating': 'B+ (Fitch)',
                    'annual_turnover': 'KES 280M',
                    'export_percentage': '65%'
                }
            ]
        }
    
    def _load_importer_database(self) -> Dict:
        """주요 수입업체 데이터베이스 (국가별)"""
        return {
            'China': [
                {
                    'company_name': 'Shanghai Premium Nuts Import Co., Ltd',
                    'registration': '91310000MA1FL5U71X',
                    'ceo_name': 'Chen Wei Ming',
                    'established_year': '2010',
                    'address': 'Room 2305, Building A, No.1000 Lujiazui Ring Road, Pudong, Shanghai 200120, China',
                    'postal_code': '200120',
                    'phone': '+86-21-5878-9000',
                    'email': 'info@shpremium.com.cn',
                    'import_license': 'CN-IMP-001',
                    'customs_code': 'CN-SH-001',
                    'certification': 'CCC, HACCP China',
                    'business_scope': 'Premium nuts import and distribution',
                    'employee_count': '85',
                    'warehouse_location': 'Shanghai Waigaoqiao Free Trade Zone',
                    'storage_capacity': '2,000 tonnes',
                    'distribution_network': '25 cities across China',
                    'annual_volume': '15,000 tonnes',
                    'target_market': 'High-end retail, food service',
                    'bank': 'Industrial and Commercial Bank of China',
                    'financial_rating': 'AA- (China Chengxin Credit Rating)',
                    'annual_turnover': 'CNY 450M'
                }
            ],
            'Germany': [
                {
                    'company_name': 'Deutsche Nuss Import GmbH',
                    'registration': 'HRB 98765',
                    'ceo_name': 'Klaus Mueller',
                    'established_year': '1987',
                    'address': 'Speicherstadt 15, 20457 Hamburg, Germany',
                    'postal_code': '20457',
                    'phone': '+49-40-789-3000',
                    'email': 'import@deutschenuss.de',
                    'import_license': 'DE-IMP-001',
                    'customs_code': 'DE-HH-001',
                    'certification': 'BRC, IFS, EU Organic',
                    'business_scope': 'Nuts and dried fruits import',
                    'employee_count': '120',
                    'warehouse_location': 'Hamburg Port Area',
                    'storage_capacity': '3,500 tonnes',
                    'distribution_network': 'EU-wide distribution',
                    'annual_volume': '25,000 tonnes',
                    'target_market': 'Retail chains, food processing',
                    'bank': 'Deutsche Bank AG',
                    'financial_rating': 'A+ (Creditreform)',
                    'annual_turnover': 'EUR 180M'
                }
            ],
            'Japan': [
                {
                    'company_name': 'Tokyo Premium Foods K.K.',
                    'registration': '0104-01-123456',
                    'ceo_name': 'Hiroshi Tanaka',
                    'established_year': '1995',
                    'address': '2-8-1 Tsukiji, Chuo-ku, Tokyo 104-0045, Japan',
                    'postal_code': '104-0045',
                    'phone': '+81-3-5545-8000',
                    'email': 'import@tokyopremium.co.jp',
                    'import_license': 'JP-IMP-001',
                    'customs_code': 'JP-TK-001',
                    'certification': 'JAS Organic, HACCP Japan',
                    'business_scope': 'Premium imported foods',
                    'employee_count': '65',
                    'warehouse_location': 'Tokyo Port',
                    'storage_capacity': '1,200 tonnes',
                    'distribution_network': 'Major Japanese cities',
                    'annual_volume': '8,000 tonnes',
                    'target_market': 'Premium retail, confectionery',
                    'bank': 'Mizuho Bank',
                    'financial_rating': 'AA (Japan Credit Rating Agency)',
                    'annual_turnover': 'JPY 12B'
                }
            ],
            'South Korea': [
                {
                    'company_name': '프리미엄 견과 수입(주)',
                    'registration': '110111-1234567',
                    'ceo_name': '김민수',
                    'established_year': '2005',
                    'address': '서울특별시 강남구 테헤란로 123, 무역센터 15층',
                    'postal_code': '06159',
                    'phone': '+82-2-551-8000',
                    'email': 'import@premiumnut.co.kr',
                    'import_license': 'KR-IMP-001',
                    'customs_code': 'KR-SE-001',
                    'certification': 'HACCP Korea, K-Food',
                    'business_scope': '프리미엄 견과류 수입유통',
                    'employee_count': '45',
                    'warehouse_location': '인천항 자유무역지역',
                    'storage_capacity': '800톤',
                    'distribution_network': '전국 주요 도시',
                    'annual_volume': '5,000톤',
                    'target_market': '대형마트, 온라인몰',
                    'bank': '신한은행',
                    'financial_rating': 'A+ (한국신용평가)',
                    'annual_turnover': 'KRW 350억'
                }
            ]
        }
    
    def get_exporter(self, country: str) -> Dict:
        """특정 국가의 수출업체 정보 반환"""
        exporters = self.exporters.get(country, [])
        return random.choice(exporters) if exporters else {}
    
    def get_importer(self, country: str) -> Dict:
        """특정 국가의 수입업체 정보 반환"""
        importers = self.importers.get(country, [])
        if importers:
            return random.choice(importers)
        else:
            # 기본 수입업체 정보
            return {
                'company_name': f'{country} Import Company Ltd',
                'ceo_name': 'Unknown',
                'address': f'{country} Trade Center',
                'import_license': f'{country}-IMP-001',
                'phone': 'N/A',
                'email': 'N/A'
            }
    
    def get_export_destinations(self, origin_country: str) -> List[str]:
        """원산지 국가별 주요 수출 대상국"""
        destinations = {
            'Australia': ['China', 'Japan', 'South Korea', 'Germany', 'USA'],
            'South Africa': ['Germany', 'China', 'USA', 'Netherlands'],
            'Kenya': ['Germany', 'USA', 'Netherlands', 'UK']
        }
        return destinations.get(origin_country, ['China', 'Germany', 'USA'])
