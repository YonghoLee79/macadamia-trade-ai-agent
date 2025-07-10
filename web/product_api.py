"""
제품 및 HS 코드 관련 API 핸들러
"""
from flask import jsonify, request
import logging
from product_database import search_products_by_name, get_hs_code_info, get_all_product_categories

logger = logging.getLogger(__name__)

class ProductAPIHandler:
    """제품 관련 API 핸들러"""
    
    def __init__(self, components):
        self.db_manager = components['db_manager']
        
    def search_products(self):
        """제품 검색"""
        try:
            query = request.args.get('q', '').strip()
            
            if not query:
                return jsonify({
                    'success': False,
                    'error': 'Search query is required'
                }), 400
            
            if len(query) < 2:
                return jsonify({
                    'success': False,
                    'error': 'Search query must be at least 2 characters'
                }), 400
            
            # 제품 검색 실행
            results = search_products_by_name(query)
            
            return jsonify({
                'success': True,
                'results': results,
                'query': query,
                'total': len(results)
            })
            
        except Exception as e:
            logger.error(f"제품 검색 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_hs_code(self):
        """HS 코드 정보 조회"""
        try:
            hs_code = request.args.get('code', '').strip()
            
            if not hs_code:
                return jsonify({
                    'success': False,
                    'error': 'HS code is required'
                }), 400
            
            # HS 코드 정보 조회
            hs_info = get_hs_code_info(hs_code)
            
            if not hs_info:
                return jsonify({
                    'success': False,
                    'error': f'HS code {hs_code} not found'
                }), 404
            
            return jsonify({
                'success': True,
                'hs_code': hs_code,
                'info': hs_info
            })
            
        except Exception as e:
            logger.error(f"HS 코드 조회 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_categories(self):
        """제품 카테고리 목록"""
        try:
            # 모든 제품 카테고리 조회
            categories = get_all_product_categories()
            
            return jsonify({
                'success': True,
                'categories': categories,
                'total': len(categories)
            })
            
        except Exception as e:
            logger.error(f"카테고리 조회 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_product_stats(self):
        """제품별 통계"""
        try:
            product_code = request.args.get('code', '').strip()
            
            if not product_code:
                return jsonify({
                    'success': False,
                    'error': 'Product code is required'
                }), 400
            
            # 제품별 통계 조회 (실제 구현에서는 DB 쿼리)
            # 여기서는 샘플 데이터 반환
            stats = {
                'product_code': product_code,
                'total_trades': 150,
                'total_value': 2500000,
                'total_quantity': 85000,
                'average_price': 29.41,
                'top_origins': [
                    {'country': 'Australia', 'percentage': 65.5},
                    {'country': 'South Africa', 'percentage': 25.2},
                    {'country': 'Kenya', 'percentage': 9.3}
                ],
                'monthly_trend': [
                    {'month': '2024-01', 'value': 180000},
                    {'month': '2024-02', 'value': 220000},
                    {'month': '2024-03', 'value': 195000},
                    {'month': '2024-04', 'value': 285000},
                    {'month': '2024-05', 'value': 310000},
                    {'month': '2024-06', 'value': 295000}
                ]
            }
            
            return jsonify({
                'success': True,
                'stats': stats
            })
            
        except Exception as e:
            logger.error(f"제품 통계 조회 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
