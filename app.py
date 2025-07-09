from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import logging
import threading
import time

# 프로젝트 모듈 import
from config import Config
from models import DatabaseManager, TradeRecord
from data_scraper import MacadamiaTradeDataScraper
from ai_agent import MacadamiaTradeAIAgent
from scheduler import MacadamiaTradeScheduler

# Flask 앱 초기화
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'macadamia-trade-secret-key')

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 전역 변수
config = Config()
db_manager = DatabaseManager(config.DATABASE_URL)
scraper = MacadamiaTradeDataScraper()
ai_agent = MacadamiaTradeAIAgent()
scheduler = MacadamiaTradeScheduler()

# 스케줄러를 백그라운드에서 실행
def run_scheduler():
    scheduler.start_scheduler()

# 백그라운드 스케줄러 시작
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/dashboard')
def dashboard_data():
    """대시보드 데이터 API"""
    try:
        # 최근 7일 데이터 가져오기
        records = db_manager.get_latest_records(7)
        
        # 기본 통계 계산
        total_records = len(records)
        total_value = sum(record.value_usd or 0 for record in records)
        
        # 국가별 통계
        country_stats = {}
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
        
        # 일별 데이터 (최근 7일)
        daily_data = {}
        for record in records:
            date_str = record.date.strftime('%Y-%m-%d')
            if date_str not in daily_data:
                daily_data[date_str] = {'value': 0, 'count': 0}
            daily_data[date_str]['value'] += record.value_usd or 0
            daily_data[date_str]['count'] += 1
        
        return jsonify({
            'success': True,
            'data': {
                'summary': {
                    'total_records': total_records,
                    'total_value': total_value,
                    'period': f"{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} ~ {datetime.now().strftime('%Y-%m-%d')}"
                },
                'top_exporters': top_exporters,
                'top_importers': top_importers,
                'daily_data': daily_data
            }
        })
        
    except Exception as e:
        logger.error(f"Dashboard data error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/analysis/<int:days>')
def get_analysis(days):
    """AI 분석 결과 API"""
    try:
        analysis = ai_agent.analyze_trade_trends(days)
        return jsonify({
            'success': True,
            'analysis': analysis,
            'days': days,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/collect', methods=['POST'])
def manual_collect():
    """수동 데이터 수집 API"""
    try:
        # 데이터 수집
        trade_data = scraper.collect_all_data()
        
        # 데이터베이스 저장
        scraper.save_to_database(trade_data)
        
        return jsonify({
            'success': True,
            'message': f'데이터 수집 완료: {len(trade_data)}건',
            'count': len(trade_data)
        })
    except Exception as e:
        logger.error(f"Manual collect error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/reports')
def get_reports():
    """저장된 보고서 목록 API"""
    try:
        import os
        reports_dir = 'reports'
        reports = []
        
        if os.path.exists(reports_dir):
            for filename in os.listdir(reports_dir):
                if filename.endswith('.md'):
                    filepath = os.path.join(reports_dir, filename)
                    stat = os.stat(filepath)
                    reports.append({
                        'filename': filename,
                        'date': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                        'size': stat.st_size
                    })
        
        reports.sort(key=lambda x: x['date'], reverse=True)
        
        return jsonify({
            'success': True,
            'reports': reports
        })
    except Exception as e:
        logger.error(f"Reports error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/report/<filename>')
def get_report_content(filename):
    """특정 보고서 내용 API"""
    try:
        filepath = os.path.join('reports', filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({
                'success': True,
                'content': content,
                'filename': filename
            })
        else:
            return jsonify({'success': False, 'error': '파일을 찾을 수 없습니다.'})
    except Exception as e:
        logger.error(f"Report content error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/status')
def get_status():
    """시스템 상태 API"""
    try:
        # 데이터베이스 연결 확인
        recent_records = db_manager.get_latest_records(1)
        last_update = recent_records[0].created_at if recent_records else None
        
        return jsonify({
            'success': True,
            'status': {
                'database': 'connected',
                'last_update': last_update.strftime('%Y-%m-%d %H:%M:%S') if last_update else 'No data',
                'scheduler': 'running',
                'total_records': len(db_manager.get_latest_records(30))
            }
        })
    except Exception as e:
        logger.error(f"Status error: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # 프로덕션 환경에서는 스케줄러 시작
    if os.getenv('FLASK_ENV') != 'development':
        scheduler_thread.start()
    
    port = int(os.getenv('PORT', 5000))
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0', port=port)
