"""
데이터베이스 관련 API 핸들러
"""
from flask import jsonify
from datetime import datetime, timedelta
import logging
import random

logger = logging.getLogger(__name__)

class DatabaseAPI:
    """데이터베이스 API 핸들러"""
    
    def __init__(self, db_manager, config):
        self.db_manager = db_manager
        self.config = config
    
    def init_database(self):
        """데이터베이스 초기화 및 샘플 데이터 생성"""
        try:
            # 기존 데이터 확인
            existing_records = self.db_manager.get_latest_records(10)
            
            if len(existing_records) > 50:
                return jsonify({
                    'success': True,
                    'message': f'데이터베이스에 이미 {len(existing_records)}개의 레코드가 있습니다.',
                    'existing_records': len(existing_records)
                })
            
            # 샘플 데이터 생성
            sample_data = self._generate_sample_data()
            
            # 데이터베이스에 저장
            saved_count = 0
            for data in sample_data:
                try:
                    saved = self.db_manager.save_record(data)
                    if saved:
                        saved_count += 1
                except Exception as e:
                    logger.error(f"Error saving sample record: {e}")
                    continue
            
            return jsonify({
                'success': True,
                'message': f'샘플 데이터 {saved_count}개가 생성되었습니다.',
                'generated': len(sample_data),
                'saved': saved_count
            })
            
        except Exception as e:
            logger.error(f"Database init error: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    def get_database_status(self):
        """데이터베이스 상태 확인"""
        try:
            # 총 레코드 수
            total_records = len(self.db_manager.get_latest_records(1000))
            
            # 최근 레코드
            recent_records = self.db_manager.get_latest_records(5)
            recent_data = []
            for record in recent_records:
                recent_data.append({
                    'id': record.id,
                    'date': record.date.isoformat() if record.date else None,
                    'product_code': record.product_code,
                    'country_origin': record.country_origin,
                    'country_destination': record.country_destination,
                    'value_usd': record.value_usd,
                    'created_at': record.created_at.isoformat() if record.created_at else None
                })
            
            # 데이터베이스 URL 정보 (민감한 정보는 마스킹)
            db_url = self.config.DATABASE_URL
            if 'postgresql' in db_url:
                db_type = 'PostgreSQL'
            elif 'sqlite' in db_url:
                db_type = 'SQLite'
            else:
                db_type = 'Unknown'
            
            return jsonify({
                'success': True,
                'database_type': db_type,
                'total_records': total_records,
                'recent_records': recent_data,
                'connection_status': 'connected'
            })
            
        except Exception as e:
            logger.error(f"Database status error: {e}")
            return jsonify({
                'success': False, 
                'error': str(e),
                'connection_status': 'error'
            })
    
    def upload_bulk_data(self, scraper):
        """대량 시뮬레이션 데이터 업로드 (개발/테스트용)"""
        try:
            from analyze_historical_data import generate_sample_trade_data
            
            # 시뮬레이션 데이터 생성
            trade_data = generate_sample_trade_data()
            
            # 데이터베이스에 저장
            saved_count = scraper.save_to_database(trade_data)
            
            return jsonify({
                'success': True,
                'message': f'시뮬레이션 데이터 업로드 완료: {saved_count}건 저장',
                'count': saved_count
            })
        except Exception as e:
            logger.error(f"Bulk data upload error: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    def _generate_sample_data(self):
        """샘플 데이터 생성 (내부 메서드)"""
        sample_data = []
        
        # 다양한 제품 및 국가 데이터
        products = [
            {'code': '0802.12', 'description': 'Raw Macadamia Nuts', 'unit': 'kg'},
            {'code': '0802.90', 'description': 'Processed Macadamia Nuts', 'unit': 'kg'},
            {'code': '0801.31', 'description': 'Fresh Cashew Nuts', 'unit': 'kg'},
            {'code': '0813.50', 'description': 'Dried Fruits Mix', 'unit': 'kg'},
            {'code': '0711.20', 'description': 'Frozen Vegetables', 'unit': 'kg'}
        ]
        
        countries = [
            {'origin': 'Australia', 'destination': 'South Korea', 'exporter': 'Macadamia Processing Co.', 'importer': 'Korean Import Co.'},
            {'origin': 'Kenya', 'destination': 'Japan', 'exporter': 'East Africa Nuts Ltd.', 'importer': 'Tokyo Trading Corp.'},
            {'origin': 'South Africa', 'destination': 'Germany', 'exporter': 'Cape Nuts Export', 'importer': 'European Food GmbH'},
            {'origin': 'Hawaii', 'destination': 'China', 'exporter': 'Hawaiian Premium Nuts', 'importer': 'Beijing Import Ltd.'},
            {'origin': 'Guatemala', 'destination': 'USA', 'exporter': 'Central America Exports', 'importer': 'US Food Imports'}
        ]
        
        # 지난 6개월간의 데이터 생성
        start_date = datetime.now() - timedelta(days=180)
        
        for i in range(100):  # 100개 샘플 레코드 생성
            date = start_date + timedelta(days=random.randint(0, 180))
            product = random.choice(products)
            country = random.choice(countries)
            quantity = random.randint(1000, 50000)
            price_per_kg = random.uniform(8, 25)  # USD per kg
            value = quantity * price_per_kg
            
            record_data = {
                'date': date.date(),
                'product_code': product['code'],
                'product_description': product['description'],
                'country_origin': country['origin'],
                'country_destination': country['destination'],
                'company_exporter': country['exporter'],
                'company_importer': country['importer'],
                'quantity': quantity,
                'unit': product['unit'],
                'value_usd': value,
                'trade_type': 'export'
            }
            
            sample_data.append(record_data)
        
        return sample_data
