"""
대시보드 관련 API 핸들러
"""
from flask import jsonify
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DashboardAPI:
    """대시보드 데이터 API 핸들러"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_dashboard_data(self):
        """대시보드 데이터 반환"""
        try:
            # 최근 1년 데이터 가져오기
            records = self.db_manager.get_latest_records(365)
            
            # 기본 통계 계산
            total_records = len(records)
            total_value = sum(record.value_usd or 0 for record in records)
            
            # 국가별 통계
            export_stats = {}
            import_stats = {}
            
            for record in records:
                # 수출국 통계
                if record.country_origin not in export_stats:
                    export_stats[record.country_origin] = {'value': 0, 'count': 0}
                export_stats[record.country_origin]['value'] += record.value_usd or 0
                export_stats[record.country_origin]['count'] += 1
                
                # 수입국 통계
                if record.country_destination not in import_stats:
                    import_stats[record.country_destination] = {'value': 0, 'count': 0}
                import_stats[record.country_destination]['value'] += record.value_usd or 0
                import_stats[record.country_destination]['count'] += 1
            
            # 상위 5개 국가
            top_exporters = sorted(export_stats.items(), key=lambda x: x[1]['value'], reverse=True)[:5]
            top_importers = sorted(import_stats.items(), key=lambda x: x[1]['value'], reverse=True)[:5]
            
            # 월별 데이터 (최근 12개월)
            monthly_data = {}
            for record in records:
                month_str = record.date.strftime('%Y-%m')
                if month_str not in monthly_data:
                    monthly_data[month_str] = {'value': 0, 'count': 0}
                monthly_data[month_str]['value'] += record.value_usd or 0
                monthly_data[month_str]['count'] += 1
            
            return jsonify({
                'success': True,
                'data': {
                    'summary': {
                        'total_records': total_records,
                        'total_value': total_value,
                        'period': f"{(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')} ~ {datetime.now().strftime('%Y-%m-%d')}"
                    },
                    'top_exporters': top_exporters,
                    'top_importers': top_importers,
                    'monthly_data': monthly_data
                }
            })
            
        except Exception as e:
            logger.error(f"Dashboard data error: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    def get_status(self):
        """시스템 상태 반환"""
        try:
            # 데이터베이스 연결 확인
            recent_records = self.db_manager.get_latest_records(1)
            last_update = recent_records[0].created_at if recent_records else None
            
            return jsonify({
                'success': True,
                'status': {
                    'database': 'connected',
                    'last_update': last_update.strftime('%Y-%m-%d %H:%M:%S') if last_update else 'No data',
                    'scheduler': 'running',
                    'total_records': len(self.db_manager.get_latest_records(30))
                }
            })
        except Exception as e:
            logger.error(f"Status error: {e}")
            return jsonify({'success': False, 'error': str(e)})
