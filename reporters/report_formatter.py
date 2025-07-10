"""
보고서 포맷터 - 텍스트 기반 보고서 생성
"""
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import os
from .base_reporter import BaseReporter

logger = logging.getLogger(__name__)

class ReportFormatter:
    """텍스트 기반 보고서 포맷터"""
    
    def __init__(self, base_reporter: BaseReporter):
        self.base_reporter = base_reporter
        
    def create_text_report(self, records: List, date_str: str) -> str:
        """기본 텍스트 보고서 생성"""
        try:
            filename = f"reports/macadamia_trade_report_{date_str}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                # 헤더
                f.write("="*80 + "\n")
                f.write(f"마카다미아 무역 일일 보고서 - {date_str}\n")
                f.write("="*80 + "\n\n")
                
                # 요약 정보
                self._write_summary(f, records)
                
                # 상세 데이터
                self._write_detailed_data(f, records)
                
                # 국가별 집계
                self._write_country_summary(f, records)
                
                # 제품별 집계
                self._write_product_summary(f, records)
                
                # 푸터
                f.write("\n" + "="*80 + "\n")
                f.write(f"보고서 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n")
            
            logger.info(f"텍스트 보고서 생성 완료: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"텍스트 보고서 생성 오류: {e}")
            return None
            
    def create_weekly_text_report(self, records: List, date_str: str) -> str:
        """주간 텍스트 보고서 생성"""
        try:
            filename = f"reports/macadamia_weekly_report_{date_str}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write(f"마카다미아 무역 주간 보고서 - {date_str}\n")
                f.write("="*80 + "\n\n")
                
                self._write_summary(f, records)
                self._write_weekly_analysis(f, records)
                self._write_country_summary(f, records)
                self._write_product_summary(f, records)
                
                f.write("\n" + "="*80 + "\n")
                f.write(f"보고서 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n")
            
            logger.info(f"주간 텍스트 보고서 생성 완료: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"주간 텍스트 보고서 생성 오류: {e}")
            return None
            
    def create_monthly_text_report(self, records: List, date_str: str) -> str:
        """월간 텍스트 보고서 생성"""
        try:
            filename = f"reports/macadamia_monthly_report_{date_str}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write(f"마카다미아 무역 월간 보고서 - {date_str}\n")
                f.write("="*80 + "\n\n")
                
                self._write_summary(f, records)
                self._write_monthly_analysis(f, records)
                self._write_country_summary(f, records)
                self._write_product_summary(f, records)
                self._write_trend_analysis(f, records)
                
                f.write("\n" + "="*80 + "\n")
                f.write(f"보고서 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n")
            
            logger.info(f"월간 텍스트 보고서 생성 완료: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"월간 텍스트 보고서 생성 오류: {e}")
            return None
            
    def create_custom_text_report(self, records: List, date_str: str) -> str:
        """사용자 정의 텍스트 보고서 생성"""
        try:
            filename = f"reports/macadamia_custom_report_{date_str}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write(f"마카다미아 무역 사용자 정의 보고서 - {date_str}\n")
                f.write("="*80 + "\n\n")
                
                self._write_summary(f, records)
                self._write_detailed_data(f, records)
                self._write_country_summary(f, records)
                self._write_product_summary(f, records)
                
                f.write("\n" + "="*80 + "\n")
                f.write(f"보고서 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n")
            
            logger.info(f"사용자 정의 텍스트 보고서 생성 완료: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"사용자 정의 텍스트 보고서 생성 오류: {e}")
            return None
            
    def _write_summary(self, f, records: List):
        """요약 정보 작성"""
        f.write("📊 요약 정보\n")
        f.write("-" * 40 + "\n")
        
        total_records = len(records)
        total_value = sum(record.trade_value for record in records if record.trade_value)
        total_quantity = sum(record.quantity for record in records if record.quantity)
        
        unique_countries = len(set(record.country_origin for record in records if record.country_origin))
        unique_products = len(set(record.product_code for record in records if record.product_code))
        
        f.write(f"총 거래 건수: {total_records:,}건\n")
        f.write(f"총 거래액: {self.base_reporter._format_currency(total_value)}\n")
        f.write(f"총 거래량: {self.base_reporter._format_quantity(total_quantity)}\n")
        f.write(f"거래 국가 수: {unique_countries}개국\n")
        f.write(f"거래 제품 수: {unique_products}개\n")
        
        if total_records > 0:
            avg_value = total_value / total_records
            f.write(f"평균 거래액: {self.base_reporter._format_currency(avg_value)}\n")
        
        f.write("\n")
        
    def _write_detailed_data(self, f, records: List):
        """상세 데이터 작성"""
        f.write("📋 상세 거래 데이터\n")
        f.write("-" * 40 + "\n")
        
        # 최근 10건만 표시
        display_records = records[:10] if len(records) > 10 else records
        
        f.write(f"{'날짜':<12} {'제품코드':<10} {'원산지':<15} {'거래액(USD)':<15} {'수량(kg)':<12} {'거래유형':<8}\n")
        f.write("-" * 80 + "\n")
        
        for record in display_records:
            date_str = record.date.strftime('%Y-%m-%d') if record.date else 'N/A'
            product_code = record.product_code[:8] if record.product_code else 'N/A'
            origin = record.country_origin[:13] if record.country_origin else 'N/A'
            value = f"{record.trade_value:,.0f}" if record.trade_value else '0'
            quantity = f"{record.quantity:,.0f}" if record.quantity else '0'
            trade_type = record.trade_type[:6] if record.trade_type else 'N/A'
            
            f.write(f"{date_str:<12} {product_code:<10} {origin:<15} {value:<15} {quantity:<12} {trade_type:<8}\n")
        
        if len(records) > 10:
            f.write(f"\n... 및 {len(records) - 10}건 추가\n")
        
        f.write("\n")
        
    def _write_country_summary(self, f, records: List):
        """국가별 집계 작성"""
        f.write("🌍 국가별 거래 현황\n")
        f.write("-" * 40 + "\n")
        
        # 국가별 집계
        country_stats = {}
        for record in records:
            if record.country_origin:
                country = record.country_origin
                if country not in country_stats:
                    country_stats[country] = {'count': 0, 'value': 0, 'quantity': 0}
                
                country_stats[country]['count'] += 1
                country_stats[country]['value'] += record.trade_value or 0
                country_stats[country]['quantity'] += record.quantity or 0
        
        # 거래액 기준 정렬
        sorted_countries = sorted(country_stats.items(), key=lambda x: x[1]['value'], reverse=True)
        
        f.write(f"{'국가':<20} {'거래건수':<10} {'총거래액(USD)':<18} {'총수량(kg)':<15}\n")
        f.write("-" * 70 + "\n")
        
        for country, stats in sorted_countries[:10]:  # 상위 10개국
            country_name = country[:18] if len(country) > 18 else country
            f.write(f"{country_name:<20} {stats['count']:<10} {stats['value']:<18,.0f} {stats['quantity']:<15,.0f}\n")
        
        f.write("\n")
        
    def _write_product_summary(self, f, records: List):
        """제품별 집계 작성"""
        f.write("📦 제품별 거래 현황\n")
        f.write("-" * 40 + "\n")
        
        # 제품별 집계
        product_stats = {}
        for record in records:
            if record.product_code:
                product = record.product_code
                if product not in product_stats:
                    product_stats[product] = {
                        'count': 0, 
                        'value': 0, 
                        'quantity': 0,
                        'description': record.product_description or 'N/A'
                    }
                
                product_stats[product]['count'] += 1
                product_stats[product]['value'] += record.trade_value or 0
                product_stats[product]['quantity'] += record.quantity or 0
        
        # 거래액 기준 정렬
        sorted_products = sorted(product_stats.items(), key=lambda x: x[1]['value'], reverse=True)
        
        f.write(f"{'제품코드':<12} {'거래건수':<10} {'총거래액(USD)':<18} {'총수량(kg)':<15}\n")
        f.write("-" * 65 + "\n")
        
        for product, stats in sorted_products:
            f.write(f"{product:<12} {stats['count']:<10} {stats['value']:<18,.0f} {stats['quantity']:<15,.0f}\n")
        
        f.write("\n")
        
    def _write_weekly_analysis(self, f, records: List):
        """주간 분석 작성"""
        f.write("📈 주간 분석\n")
        f.write("-" * 40 + "\n")
        
        if not records:
            f.write("분석할 데이터가 없습니다.\n\n")
            return
        
        # 일별 집계 (최근 7일)
        daily_stats = {}
        for record in records:
            if record.date:
                date_key = record.date.strftime('%Y-%m-%d')
                if date_key not in daily_stats:
                    daily_stats[date_key] = {'count': 0, 'value': 0}
                
                daily_stats[date_key]['count'] += 1
                daily_stats[date_key]['value'] += record.trade_value or 0
        
        f.write("일별 거래 현황 (최근 7일):\n")
        for date_key in sorted(daily_stats.keys()):
            stats = daily_stats[date_key]
            f.write(f"  {date_key}: {stats['count']}건, ${stats['value']:,.0f}\n")
        
        f.write("\n")
        
    def _write_monthly_analysis(self, f, records: List):
        """월간 분석 작성"""
        f.write("📊 월간 분석\n")
        f.write("-" * 40 + "\n")
        
        if not records:
            f.write("분석할 데이터가 없습니다.\n\n")
            return
        
        # 주별 집계
        weekly_stats = {}
        for record in records:
            if record.date:
                # 주차 계산 (간단히 일자를 7로 나눈 몫 사용)
                week_num = (record.date.day - 1) // 7 + 1
                week_key = f"Week {week_num}"
                
                if week_key not in weekly_stats:
                    weekly_stats[week_key] = {'count': 0, 'value': 0}
                
                weekly_stats[week_key]['count'] += 1
                weekly_stats[week_key]['value'] += record.trade_value or 0
        
        f.write("주별 거래 현황:\n")
        for week_key in sorted(weekly_stats.keys()):
            stats = weekly_stats[week_key]
            f.write(f"  {week_key}: {stats['count']}건, ${stats['value']:,.0f}\n")
        
        f.write("\n")
        
    def _write_trend_analysis(self, f, records: List):
        """트렌드 분석 작성"""
        f.write("📈 트렌드 분석\n")
        f.write("-" * 40 + "\n")
        
        if len(records) < 2:
            f.write("트렌드 분석을 위한 충분한 데이터가 없습니다.\n\n")
            return
        
        # 간단한 트렌드 분석
        total_value = sum(record.trade_value for record in records if record.trade_value)
        total_quantity = sum(record.quantity for record in records if record.quantity)
        
        if total_value > 0:
            avg_price = total_value / total_quantity if total_quantity > 0 else 0
            f.write(f"평균 단가: ${avg_price:.2f}/kg\n")
        
        # 최대/최소 거래
        max_trade = max(records, key=lambda x: x.trade_value or 0)
        min_trade = min(records, key=lambda x: x.trade_value or 0)
        
        f.write(f"최대 거래: ${max_trade.trade_value:,.0f} ({max_trade.country_origin})\n")
        f.write(f"최소 거래: ${min_trade.trade_value:,.0f} ({min_trade.country_origin})\n")
        
        f.write("\n")
