from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import logging
import threading
import time
import random

# 프로젝트 모듈 import
from config import Config
from models import DatabaseManager, TradeRecord
from data_scraper import MacadamiaTradeDataScraper
from ai_agent import MacadamiaTradeAIAgent
from scheduler import MacadamiaTradeScheduler
from telegram_notifier import send_system_alert, send_new_data_alert, send_analysis_summary, send_daily_summary
from product_database import search_products_by_name, get_hs_code_info, get_all_product_categories

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

# AI Agent 초기화 (실패해도 앱은 시작되도록)
try:
    ai_agent = MacadamiaTradeAIAgent()
    logger.info("AI Agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize AI Agent: {e}")
    ai_agent = None

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

@app.route('/health')
def health_check():
    """Railway 헬스체크용 엔드포인트"""
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }, 200

@app.route('/api/dashboard')
def dashboard_data():
    """대시보드 데이터 API"""
    try:
        # 최근 1년 데이터 가져오기
        records = db_manager.get_latest_records(365)
        
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

@app.route('/api/analysis/<int:days>')
def get_analysis(days):
    """AI 분석 결과 API"""
    try:
        if ai_agent is None:
            return jsonify({
                'success': False, 
                'error': 'AI Agent not available (OpenAI API key issue)'
            })
        
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
        # 데이터 수집 (알림 포함)
        result = scraper.collect_and_notify()
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f'데이터 수집 완료: {result["saved"]}건 저장',
                'count': result['saved'],
                'collected': result['collected'],
                'duration': result['duration']
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error')
            })
    except Exception as e:
        logger.error(f"Manual collect error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/telegram/test', methods=['POST'])
def test_telegram():
    """텔레그램 연결 테스트 API"""
    try:
        # 테스트 메시지 전송
        success = send_system_alert(
            'info',
            '마카다미아 무역 AI 에이전트 텔레그램 연결 테스트입니다. 🌰'
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': '텔레그램 연결 테스트 성공!'
            })
        else:
            return jsonify({
                'success': False,
                'error': '텔레그램 메시지 전송 실패'
            })
    except Exception as e:
        logger.error(f"Telegram test error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/telegram/summary', methods=['POST'])
def send_manual_summary():
    """수동 일일 요약 전송 API"""
    try:
        # 요약 데이터 생성
        records = db_manager.get_latest_records(1)
        
        total_records = len(records)
        total_value = sum(record.value_usd or 0 for record in records)
        
        country_stats = {}
        for record in records:
            country = record.country_origin
            if country not in country_stats:
                country_stats[country] = {'value': 0, 'count': 0}
            country_stats[country]['value'] += record.value_usd or 0
            country_stats[country]['count'] += 1
        
        top_countries = sorted(country_stats.items(), key=lambda x: x[1]['value'], reverse=True)[:5]
        
        summary_data = {
            'total_records': total_records,
            'total_value': total_value,
            'top_countries': top_countries,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        # 텔레그램으로 전송
        success = send_daily_summary(summary_data)
        
        if success:
            return jsonify({
                'success': True,
                'message': '일일 요약이 텔레그램으로 전송되었습니다.'
            })
        else:
            return jsonify({
                'success': False,
                'error': '텔레그램 전송 실패'
            })
    except Exception as e:
        logger.error(f"Manual summary error: {e}")
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

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """새로운 마카다미아 무역 보고서 생성 API"""
    try:
        if ai_agent is None:
            return jsonify({
                'success': False, 
                'error': 'AI Agent not available (OpenAI API key issue)'
            })
        
        # AI 보고서 생성
        report = ai_agent.generate_daily_report()
        
        # 보고서 파일로 저장
        date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"macadamia_report_{date_str}.md"
        filepath = os.path.join('reports', filename)
        
        os.makedirs("reports", exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"보고서 생성 및 저장 완료: {filepath}")
        
        return jsonify({
            'success': True,
            'message': f'보고서가 생성되었습니다: {filename}',
            'filename': filename
        })
        
    except Exception as e:
        logger.error(f"보고서 생성 오류: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/generate-sample-report', methods=['POST'])
def generate_sample_report():
    """샘플 보고서 생성 API (AI Agent 없이도 작동)"""
    try:
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
        
        logger.info(f"샘플 보고서 생성 완료: {filepath}")
        
        return jsonify({
            'success': True,
            'message': f'샘플 보고서가 생성되었습니다: {filename}',
            'filename': filename
        })
        
    except Exception as e:
        logger.error(f"샘플 보고서 생성 오류: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/products/search')
def search_products():
    """제품 검색 API"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'success': False, 'error': '검색어를 입력해주세요.'})
        
        results = search_products_by_name(query)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results
        })
    except Exception as e:
        logger.error(f"Product search error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/products/categories')
def get_product_categories():
    """제품 카테고리 목록 API"""
    try:
        categories = get_all_product_categories()
        
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        logger.error(f"Product categories error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/hscode/<hs_code>')
def get_hscode_info(hs_code):
    """HS 코드 상세 정보 API"""
    try:
        if not hs_code or len(hs_code) < 4:
            return jsonify({'success': False, 'error': '유효한 HS 코드를 입력해주세요.'})
        
        info = get_hs_code_info(hs_code)
        
        return jsonify({
            'success': True,
            'hs_code': hs_code,
            'info': info
        })
    except Exception as e:
        logger.error(f"HS code info error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/products/bulk-data', methods=['POST'])
def upload_bulk_data():
    """대량 시뮬레이션 데이터 업로드 API (개발/테스트용)"""
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

@app.route('/api/init-database', methods=['POST'])
def init_database():
    """데이터베이스 초기화 및 샘플 데이터 생성 API"""
    try:
        # 기존 데이터 확인
        existing_records = db_manager.get_latest_records(10)
        
        if len(existing_records) > 50:
            return jsonify({
                'success': True,
                'message': f'데이터베이스에 이미 {len(existing_records)}개의 레코드가 있습니다.',
                'existing_records': len(existing_records)
            })
        
        # 샘플 데이터 생성
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
        
        # 데이터베이스에 저장
        saved_count = 0
        for data in sample_data:
            try:
                saved = db_manager.save_record(data)
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

@app.route('/api/database/status')
def database_status():
    """데이터베이스 상태 확인 API"""
    try:
        # 총 레코드 수
        total_records = len(db_manager.get_latest_records(1000))
        
        # 최근 레코드
        recent_records = db_manager.get_latest_records(5)
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
        db_url = config.DATABASE_URL
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

if __name__ == '__main__':
    # 프로덕션 환경에서는 스케줄러 시작
    if os.getenv('FLASK_ENV') != 'development':
        scheduler_thread.start()
    
    # Railway 포트 설정 처리
    try:
        port = int(os.getenv('PORT', '5000'))
    except (ValueError, TypeError):
        port = 5000
        logger.warning(f"Invalid PORT value: {os.getenv('PORT')}, using default 5000")
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0', port=port)
