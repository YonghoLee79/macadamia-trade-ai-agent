"""
보고서 관련 API 핸들러
"""
from flask import jsonify, request, send_file
import logging
import os
from datetime import datetime, timedelta
from reporters import MacadamiaTradeExcelReporter

logger = logging.getLogger(__name__)

class ReportAPIHandler:
    """보고서 관련 API 핸들러"""
    
    def __init__(self, components):
        self.db_manager = components['db_manager']
        self.excel_reporter = MacadamiaTradeExcelReporter()
        
    def generate_report(self):
        """보고서 생성"""
        try:
            report_type = request.args.get('type', 'daily')
            date_str = request.args.get('date')
            
            if not date_str:
                date_str = datetime.now().strftime('%Y%m%d')
            
            # 보고서 타입에 따라 다른 생성 함수 호출
            if report_type == 'daily':
                filename = self.excel_reporter.generate_daily_excel_report(date_str)
            elif report_type == 'weekly':
                filename = self.excel_reporter.generate_weekly_report()
            elif report_type == 'monthly':
                filename = self.excel_reporter.generate_monthly_report()
            else:
                return jsonify({
                    'success': False,
                    'error': f'Unsupported report type: {report_type}'
                }), 400
            
            if not filename:
                return jsonify({
                    'success': False,
                    'error': 'Failed to generate report'
                }), 500
            
            # 파일명만 반환 (보안상 전체 경로는 노출하지 않음)
            report_filename = os.path.basename(filename)
            
            return jsonify({
                'success': True,
                'message': f'{report_type.title()} report generated successfully',
                'filename': report_filename,
                'download_url': f'/api/reports/{report_filename}'
            })
            
        except Exception as e:
            logger.error(f"보고서 생성 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def list_reports(self):
        """보고서 목록 조회"""
        try:
            reports_dir = 'reports'
            
            if not os.path.exists(reports_dir):
                return jsonify({
                    'success': True,
                    'reports': [],
                    'total': 0
                })
            
            # 보고서 파일 목록 조회
            report_files = []
            for filename in os.listdir(reports_dir):
                if filename.endswith(('.xlsx', '.txt', '.csv')):
                    filepath = os.path.join(reports_dir, filename)
                    stat = os.stat(filepath)
                    
                    report_files.append({
                        'filename': filename,
                        'size': stat.st_size,
                        'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'download_url': f'/api/reports/{filename}'
                    })
            
            # 수정 시간 기준 내림차순 정렬
            report_files.sort(key=lambda x: x['modified_at'], reverse=True)
            
            return jsonify({
                'success': True,
                'reports': report_files,
                'total': len(report_files)
            })
            
        except Exception as e:
            logger.error(f"보고서 목록 조회 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def download_report(self, filename):
        """보고서 파일 다운로드"""
        try:
            # 보안 검증: 파일명에 경로 조작 문자가 있는지 확인
            if '..' in filename or '/' in filename or '\\' in filename:
                return jsonify({
                    'success': False,
                    'error': 'Invalid filename'
                }), 400
            
            filepath = os.path.join('reports', filename)
            
            # 파일 존재 확인
            if not os.path.exists(filepath):
                return jsonify({
                    'success': False,
                    'error': 'Report file not found'
                }), 404
            
            # 파일 다운로드
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            logger.error(f"보고서 다운로드 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def delete_report(self, filename):
        """보고서 파일 삭제"""
        try:
            # 보안 검증
            if '..' in filename or '/' in filename or '\\' in filename:
                return jsonify({
                    'success': False,
                    'error': 'Invalid filename'
                }), 400
            
            filepath = os.path.join('reports', filename)
            
            # 파일 존재 확인
            if not os.path.exists(filepath):
                return jsonify({
                    'success': False,
                    'error': 'Report file not found'
                }), 404
            
            # 파일 삭제
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'message': f'Report {filename} deleted successfully'
            })
            
        except Exception as e:
            logger.error(f"보고서 삭제 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_report_stats(self):
        """보고서 통계"""
        try:
            reports_dir = 'reports'
            
            if not os.path.exists(reports_dir):
                return jsonify({
                    'success': True,
                    'stats': {
                        'total_reports': 0,
                        'total_size': 0,
                        'by_type': {},
                        'recent_reports': []
                    }
                })
            
            # 보고서 통계 계산
            total_reports = 0
            total_size = 0
            by_type = {}
            recent_reports = []
            
            for filename in os.listdir(reports_dir):
                if filename.endswith(('.xlsx', '.txt', '.csv')):
                    filepath = os.path.join(reports_dir, filename)
                    stat = os.stat(filepath)
                    
                    total_reports += 1
                    total_size += stat.st_size
                    
                    # 파일 확장자별 분류
                    ext = filename.split('.')[-1]
                    by_type[ext] = by_type.get(ext, 0) + 1
                    
                    # 최근 5개 보고서
                    if len(recent_reports) < 5:
                        recent_reports.append({
                            'filename': filename,
                            'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat()
                        })
            
            # 최근 보고서 정렬
            recent_reports.sort(key=lambda x: x['created_at'], reverse=True)
            
            return jsonify({
                'success': True,
                'stats': {
                    'total_reports': total_reports,
                    'total_size': total_size,
                    'total_size_mb': round(total_size / (1024 * 1024), 2),
                    'by_type': by_type,
                    'recent_reports': recent_reports[:5]
                }
            })
            
        except Exception as e:
            logger.error(f"보고서 통계 조회 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
