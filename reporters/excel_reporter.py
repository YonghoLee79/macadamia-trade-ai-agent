"""
보고서 생성 메인 클래스
"""
import logging
from datetime import datetime
from typing import List, Dict
import os
from .base_reporter import BaseReporter
from .excel_processor import ExcelDataProcessor
from .chart_generator import ChartGenerator
from .report_formatter import ReportFormatter

logger = logging.getLogger(__name__)

class MacadamiaTradeExcelReporter:
    """마카다미아 무역 Excel 보고서 생성기 메인 클래스"""
    
    def __init__(self):
        self.base_reporter = BaseReporter()
        self.excel_processor = ExcelDataProcessor(self.base_reporter)
        self.chart_generator = ChartGenerator(self.base_reporter)
        self.formatter = ReportFormatter(self.base_reporter)
        
    def generate_daily_excel_report(self, date_str: str = None) -> str:
        """일일 엑셀 보고서 생성"""
        if date_str is None:
            date_str = datetime.now().strftime('%Y%m%d')
        
        try:
            logger.info(f"일일 보고서 생성 시작: {date_str}")
            
            # 보고서 디렉토리 확인
            self.base_reporter._ensure_reports_directory()
            
            # 최근 데이터 가져오기
            records = self.base_reporter.db.get_latest_records(100)
            
            if not records:
                logger.warning("보고서 생성할 데이터가 없습니다.")
                return None
            
            # 엑셀 파일 생성
            filename = f"reports/macadamia_trade_report_{date_str}.xlsx"
            
            try:
                # pandas가 설치된 경우
                import pandas as pd
                
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    # 1. 원본 데이터 시트
                    self.excel_processor.create_raw_data_sheet(records, writer)
                    
                    # 2. 국가별 요약 시트
                    self.excel_processor.create_country_summary_sheet(records, writer)
                    
                    # 3. 제품별 요약 시트
                    self.excel_processor.create_product_summary_sheet(records, writer)
                    
                    # 4. 월별 트렌드 시트
                    self.excel_processor.create_monthly_trend_sheet(writer)
                    
                    # 5. 데이터 입력 템플릿 시트
                    self.excel_processor.create_input_template_sheet(writer)
                    
                    # 6. 차트 및 분석 (선택적)
                    self.chart_generator.create_charts(records, writer)
                
                logger.info(f"Excel 보고서 생성 완료: {filename}")
                
            except ImportError:
                logger.warning("pandas/openpyxl이 설치되지 않음. 텍스트 보고서로 대체")
                # 텍스트 기반 보고서 생성
                filename = self.formatter.create_text_report(records, date_str)
                
            return filename
            
        except Exception as e:
            logger.error(f"일일 보고서 생성 오류: {e}")
            return None
    
    def generate_weekly_report(self) -> str:
        """주간 보고서 생성"""
        try:
            logger.info("주간 보고서 생성 시작")
            
            # 최근 7일 데이터 조회
            from datetime import timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            records = self.base_reporter._get_date_range_records(start_date, end_date)
            
            if not records:
                logger.warning("주간 보고서 생성할 데이터가 없습니다.")
                return None
            
            date_str = datetime.now().strftime('%Y%m%d')
            filename = f"reports/macadamia_weekly_report_{date_str}.xlsx"
            
            try:
                import pandas as pd
                
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    self.excel_processor.create_raw_data_sheet(records, writer)
                    self.excel_processor.create_country_summary_sheet(records, writer)
                    self.excel_processor.create_product_summary_sheet(records, writer)
                    self.chart_generator.create_weekly_charts(records, writer)
                
                logger.info(f"주간 보고서 생성 완료: {filename}")
                
            except ImportError:
                filename = self.formatter.create_weekly_text_report(records, date_str)
                
            return filename
            
        except Exception as e:
            logger.error(f"주간 보고서 생성 오류: {e}")
            return None
    
    def generate_monthly_report(self) -> str:
        """월간 보고서 생성"""
        try:
            logger.info("월간 보고서 생성 시작")
            
            # 최근 30일 데이터 조회
            from datetime import timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            records = self.base_reporter._get_date_range_records(start_date, end_date)
            
            if not records:
                logger.warning("월간 보고서 생성할 데이터가 없습니다.")
                return None
            
            date_str = datetime.now().strftime('%Y%m')
            filename = f"reports/macadamia_monthly_report_{date_str}.xlsx"
            
            try:
                import pandas as pd
                
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    self.excel_processor.create_raw_data_sheet(records, writer)
                    self.excel_processor.create_country_summary_sheet(records, writer)
                    self.excel_processor.create_product_summary_sheet(records, writer)
                    self.excel_processor.create_monthly_trend_sheet(writer)
                    self.chart_generator.create_monthly_charts(records, writer)
                
                logger.info(f"월간 보고서 생성 완료: {filename}")
                
            except ImportError:
                filename = self.formatter.create_monthly_text_report(records, date_str)
                
            return filename
            
        except Exception as e:
            logger.error(f"월간 보고서 생성 오류: {e}")
            return None
    
    def generate_custom_report(self, start_date: datetime, end_date: datetime, 
                             report_type: str = "custom") -> str:
        """사용자 정의 기간 보고서 생성"""
        try:
            logger.info(f"사용자 정의 보고서 생성: {start_date} ~ {end_date}")
            
            records = self.base_reporter._get_date_range_records(start_date, end_date)
            
            if not records:
                logger.warning("사용자 정의 보고서 생성할 데이터가 없습니다.")
                return None
            
            date_str = f"{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}"
            filename = f"reports/macadamia_{report_type}_report_{date_str}.xlsx"
            
            try:
                import pandas as pd
                
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    self.excel_processor.create_raw_data_sheet(records, writer)
                    self.excel_processor.create_country_summary_sheet(records, writer)
                    self.excel_processor.create_product_summary_sheet(records, writer)
                    self.chart_generator.create_custom_charts(records, writer, start_date, end_date)
                
                logger.info(f"사용자 정의 보고서 생성 완료: {filename}")
                
            except ImportError:
                filename = self.formatter.create_custom_text_report(records, date_str)
                
            return filename
            
        except Exception as e:
            logger.error(f"사용자 정의 보고서 생성 오류: {e}")
            return None
    
    def close(self):
        """리소스 정리"""
        if self.base_reporter:
            self.base_reporter.close()
