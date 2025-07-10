"""
AI 분석 관련 API 핸들러
"""
from flask import jsonify, request
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class AIAPIHandler:
    """AI 분석 관련 API 핸들러"""
    
    def __init__(self, components):
        self.ai_agent = components['ai_agent']
        self.db_manager = components['db_manager']
        
    def analyze_data(self):
        """AI 데이터 분석"""
        try:
            if not self.ai_agent:
                return jsonify({
                    'success': False,
                    'error': 'AI Agent not available'
                }), 503
            
            # 최신 데이터 가져오기
            records = self.db_manager.get_latest_records(100)
            
            if not records:
                return jsonify({
                    'success': False,
                    'error': 'No data available for analysis'
                }), 404
            
            # AI 분석 실행
            analysis_result = self.ai_agent.analyze_trade_patterns(records)
            
            return jsonify({
                'success': True,
                'analysis': analysis_result
            })
            
        except Exception as e:
            logger.error(f"AI 분석 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def chat_with_ai(self):
        """AI 챗봇 대화"""
        try:
            if not self.ai_agent:
                return jsonify({
                    'success': False,
                    'error': 'AI Agent not available'
                }), 503
            
            data = request.get_json()
            if not data or 'message' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Message is required'
                }), 400
            
            user_message = data['message']
            
            # AI 응답 생성
            ai_response = self.ai_agent.chat_with_user(user_message)
            
            return jsonify({
                'success': True,
                'response': ai_response
            })
            
        except Exception as e:
            logger.error(f"AI 챗봇 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def predict_trends(self):
        """무역 트렌드 예측"""
        try:
            if not self.ai_agent:
                return jsonify({
                    'success': False,
                    'error': 'AI Agent not available'
                }), 503
            
            # 과거 데이터를 기반으로 트렌드 예측
            records = self.db_manager.get_latest_records(500)  # 더 많은 데이터 필요
            
            if len(records) < 10:
                return jsonify({
                    'success': False,
                    'error': 'Insufficient data for trend prediction'
                }), 404
            
            # 트렌드 예측 실행
            prediction_result = self.ai_agent.predict_trade_trends(records)
            
            return jsonify({
                'success': True,
                'predictions': prediction_result
            })
            
        except Exception as e:
            logger.error(f"트렌드 예측 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def market_insights(self):
        """시장 인사이트 생성"""
        try:
            if not self.ai_agent:
                return jsonify({
                    'success': False,
                    'error': 'AI Agent not available'
                }), 503
            
            # 시장 분석을 위한 데이터 수집
            records = self.db_manager.get_latest_records(200)
            
            if not records:
                return jsonify({
                    'success': False,
                    'error': 'No data available for market analysis'
                }), 404
            
            # 시장 인사이트 생성
            insights = self.ai_agent.generate_market_insights(records)
            
            return jsonify({
                'success': True,
                'insights': insights
            })
            
        except Exception as e:
            logger.error(f"시장 인사이트 생성 오류: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_analysis(self, days):
        """AI 분석 결과 반환"""
        try:
            if not self.ai_agent:
                return jsonify({
                    'success': False, 
                    'error': 'AI Agent not available (OpenAI API key issue)'
                })
            
            analysis = self.ai_agent.analyze_trade_trends(days)
            return jsonify({
                'success': True,
                'analysis': analysis,
                'days': days,
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    def get_ai_insights(self):
        """AI 인사이트 반환"""
        try:
            request_data = request.get_json() or {}
            return self.market_insights()
        except Exception as e:
            logger.error(f"AI insights error: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    def get_ai_predictions(self):
        """AI 예측 반환"""
        try:
            request_data = request.get_json() or {}
            return self.predict_trends()
        except Exception as e:
            logger.error(f"AI predictions error: {e}")
            return jsonify({'success': False, 'error': str(e)})
