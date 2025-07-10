"""
API 라우트 핸들러 - 데이터 수집 및 조회
"""
from flask import jsonify, request
import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class DataAPIHandler:
    """데이터 관련 API 핸들러"""
    
    def __init__(self, components):
        self.db_manager = components['db_manager']
        self.scraper = components['scraper']
        self.ai_agent = components['ai_agent']
        
    def get_latest_data(self):
        """최신 무역 데이터 조회"""
        try:
            records = self.db_manager.get_latest_records(50)
            
            data = []
            for record in records:
                data.append({
                    'id': record.id,
                    'date': record.date.isoformat() if record.date else None,
                    'product_code': record.product_code,
                    'product_description': record.product_description,
                    'country_origin': record.country_origin,
                    'country_destination': record.country_destination,
                    'trade_value': record.trade_value,
                    'quantity': record.quantity,
                    'trade_type': record.trade_type,
                    'source': record.source
                })
            
            return jsonify({
                'success': True,
                'data': data,
                'total': len(data)
            })
            
        except Exception as e:
            logger.error(f"최신 데이터 조회 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def manual_collect(self):
        """수동 데이터 수집"""
        try:
            # 데이터 수집 (알림 포함)
            result = self.scraper.collect_all_real_data()
            
            if result.get('total_collected', 0) > 0:
                return jsonify({
                    'success': True,
                    'message': f'데이터 수집 완료: {result["total_collected"]}건 수집',
                    'total_collected': result['total_collected'],
                    'sources_used': result['sources_used'],
                    'errors': result.get('errors', [])
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('errors', ['데이터 수집 실패'])
                })
        except Exception as e:
            logger.error(f"Manual collect error: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    def collect_data(self):
        """수동 데이터 수집"""
        try:
            logger.info("수동 데이터 수집 요청 받음")
            
            # 백그라운드에서 데이터 수집 시작
            import threading
            
            def collect_data_async():
                try:
                    stats = self.scraper.collect_all_real_data()
                    logger.info(f"수동 데이터 수집 완료: {stats}")
                except Exception as e:
                    logger.error(f"수동 데이터 수집 오류: {e}")
            
            thread = threading.Thread(target=collect_data_async)
            thread.start()
            
            return jsonify({
                'success': True,
                'message': 'Data collection started in background'
            })
            
        except Exception as e:
            logger.error(f"수동 데이터 수집 시작 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_monthly_chart_data(self):
        """월별 차트 데이터"""
        try:
            # 최근 12개월 데이터 조회
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            
            # 실제 구현에서는 DB에서 월별 집계 조회
            # 여기서는 샘플 데이터 생성
            months = []
            values = []
            
            for i in range(12):
                month_date = start_date + timedelta(days=30*i)
                months.append(month_date.strftime('%Y-%m'))
                values.append(random.randint(100000, 500000))
            
            return jsonify({
                'success': True,
                'data': {
                    'months': months,
                    'values': values,
                    'label': 'Monthly Trade Value (USD)'
                }
            })
            
        except Exception as e:
            logger.error(f"월별 차트 데이터 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def generate_sample_data(self):
        """샘플 데이터 생성 (테스트용)"""
        try:
            logger.info("샘플 데이터 생성 요청")
            
            # 테스트 환경에서만 허용
            import os
            if os.getenv('RAILWAY_ENVIRONMENT'):
                return jsonify({
                    'success': False,
                    'error': 'Sample data generation not allowed in production'
                }), 403
            
            # 시뮬레이션 데이터 생성
            stats = self.scraper.collect_simulation_data_for_testing()
            
            return jsonify({
                'success': True,
                'message': 'Sample data generated',
                'stats': stats
            })
            
        except Exception as e:
            logger.error(f"샘플 데이터 생성 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def upload_data(self):
        """CSV 데이터 업로드"""
        try:
            if 'file' not in request.files:
                return jsonify({
                    'success': False,
                    'error': 'No file uploaded'
                }), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({
                    'success': False,
                    'error': 'No file selected'
                }), 400
            
            if not file.filename.endswith('.csv'):
                return jsonify({
                    'success': False,
                    'error': 'Only CSV files are allowed'
                }), 400
            
            # CSV 파일 처리 (pandas가 있는 경우)
            try:
                import pandas as pd
                import io
                
                # 파일 내용 읽기
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                df = pd.read_csv(stream)
                
                # 필수 컬럼 확인
                required_columns = ['product_code', 'country_origin', 'trade_value']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    return jsonify({
                        'success': False,
                        'error': f'Missing required columns: {missing_columns}'
                    }), 400
                
                # 데이터 저장
                saved_count = 0
                for _, row in df.iterrows():
                    try:
                        from models import TradeRecord
                        record = TradeRecord(
                            product_code=row.get('product_code', ''),
                            product_description=row.get('product_description', ''),
                            country_origin=row.get('country_origin', ''),
                            country_destination=row.get('country_destination', 'Korea'),
                            trade_value=float(row.get('trade_value', 0)),
                            quantity=float(row.get('quantity', 0)),
                            trade_type=row.get('trade_type', 'import'),
                            period=row.get('period', datetime.now().strftime('%Y%m')),
                            year=int(row.get('year', datetime.now().year)),
                            source='Manual_Upload'
                        )
                        
                        record_id = self.db_manager.save_trade_record(record)
                        if record_id:
                            saved_count += 1
                            
                    except Exception as e:
                        logger.error(f"레코드 저장 오류: {e}")
                        continue
                
                return jsonify({
                    'success': True,
                    'message': f'{saved_count} records uploaded successfully',
                    'total_rows': len(df),
                    'saved_count': saved_count
                })
                
            except ImportError:
                return jsonify({
                    'success': False,
                    'error': 'CSV processing not available (pandas not installed)'
                }), 500
            
        except Exception as e:
            logger.error(f"데이터 업로드 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
