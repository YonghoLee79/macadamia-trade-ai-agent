"""
Excel 보고서 생성기
"""
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import os
from .base_reporter import BaseReporter

logger = logging.getLogger(__name__)

class ExcelDataProcessor:
    """Excel 데이터 처리 전용 클래스"""
    
    def __init__(self, base_reporter: BaseReporter):
        self.base_reporter = base_reporter
        
    def create_raw_data_sheet(self, records: List, writer):
        """원본 데이터 시트 생성"""
        try:
            # pandas가 설치되어 있는 경우에만 실행
            import pandas as pd
            from openpyxl.utils.dataframe import dataframe_to_rows
            
            df = self.base_reporter._create_dataframe_from_records(records)
            df.to_excel(writer, sheet_name='Raw Data', index=False)
            
            # 스타일 적용
            worksheet = writer.sheets['Raw Data']
            self.base_reporter._apply_header_style(worksheet, len(df.columns))
            
            logger.info("원본 데이터 시트 생성 완료")
            
        except ImportError:
            logger.warning("pandas/openpyxl이 설치되지 않음. CSV 형태로 대체 생성")
            self._create_csv_fallback(records, writer)
        except Exception as e:
            logger.error(f"원본 데이터 시트 생성 오류: {e}")
            
    def create_country_summary_sheet(self, records: List, writer):
        """국가별 요약 시트 생성"""
        try:
            import pandas as pd
            
            df = self.base_reporter._create_dataframe_from_records(records)
            
            # 국가별 집계
            country_summary = df.groupby('Origin Country').agg({
                'Trade Value (USD)': ['sum', 'count', 'mean'],
                'Quantity (kg)': 'sum'
            }).round(2)
            
            country_summary.columns = ['Total Value', 'Transaction Count', 'Average Value', 'Total Quantity']
            country_summary = country_summary.reset_index()
            
            country_summary.to_excel(writer, sheet_name='Country Summary', index=False)
            
            # 스타일 적용
            worksheet = writer.sheets['Country Summary']
            self.base_reporter._apply_header_style(worksheet, len(country_summary.columns))
            
            logger.info("국가별 요약 시트 생성 완료")
            
        except ImportError:
            logger.warning("pandas가 설치되지 않음. 국가별 요약 건너뜀")
        except Exception as e:
            logger.error(f"국가별 요약 시트 생성 오류: {e}")
            
    def create_product_summary_sheet(self, records: List, writer):
        """제품별 요약 시트 생성"""
        try:
            import pandas as pd
            
            df = self.base_reporter._create_dataframe_from_records(records)
            
            # 제품별 집계
            product_summary = df.groupby(['Product Code', 'Product Description']).agg({
                'Trade Value (USD)': ['sum', 'count'],
                'Quantity (kg)': 'sum'
            }).round(2)
            
            product_summary.columns = ['Total Value', 'Transaction Count', 'Total Quantity']
            product_summary = product_summary.reset_index()
            
            product_summary.to_excel(writer, sheet_name='Product Summary', index=False)
            
            # 스타일 적용
            worksheet = writer.sheets['Product Summary']
            self.base_reporter._apply_header_style(worksheet, len(product_summary.columns))
            
            logger.info("제품별 요약 시트 생성 완료")
            
        except ImportError:
            logger.warning("pandas가 설치되지 않음. 제품별 요약 건너뜀")
        except Exception as e:
            logger.error(f"제품별 요약 시트 생성 오류: {e}")
            
    def create_monthly_trend_sheet(self, writer):
        """월별 트렌드 시트 생성"""
        try:
            import pandas as pd
            
            # 최근 12개월 데이터 조회
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            
            records = self.base_reporter._get_date_range_records(start_date, end_date)
            
            if not records:
                logger.warning("월별 트렌드 데이터 없음")
                return
                
            df = self.base_reporter._create_dataframe_from_records(records)
            
            # 날짜를 월별로 그룹화
            df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
            
            monthly_trend = df.groupby('Month').agg({
                'Trade Value (USD)': 'sum',
                'Quantity (kg)': 'sum',
                'Product Code': 'count'
            }).round(2)
            
            monthly_trend.columns = ['Monthly Value', 'Monthly Quantity', 'Transaction Count']
            monthly_trend = monthly_trend.reset_index()
            
            monthly_trend.to_excel(writer, sheet_name='Monthly Trend', index=False)
            
            # 스타일 적용
            worksheet = writer.sheets['Monthly Trend']
            self.base_reporter._apply_header_style(worksheet, len(monthly_trend.columns))
            
            logger.info("월별 트렌드 시트 생성 완료")
            
        except ImportError:
            logger.warning("pandas가 설치되지 않음. 월별 트렌드 건너뜀")
        except Exception as e:
            logger.error(f"월별 트렌드 시트 생성 오류: {e}")
            
    def create_input_template_sheet(self, writer):
        """데이터 입력 템플릿 시트 생성"""
        try:
            import pandas as pd
            
            # 템플릿 구조 정의
            template_columns = [
                'Date (YYYY-MM-DD)',
                'Product Code',
                'Product Description',
                'Origin Country',
                'Destination Country',
                'Trade Value (USD)',
                'Quantity (kg)',
                'Trade Type (import/export)',
                'Period',
                'Year',
                'Source'
            ]
            
            # 빈 템플릿 생성
            template_df = pd.DataFrame(columns=template_columns)
            
            # 샘플 데이터 한 줄 추가
            sample_row = {
                'Date (YYYY-MM-DD)': '2024-07-10',
                'Product Code': '080250',
                'Product Description': 'Macadamia nuts in shell',
                'Origin Country': 'Australia',
                'Destination Country': 'Korea',
                'Trade Value (USD)': '150000',
                'Quantity (kg)': '5000',
                'Trade Type (import/export)': 'import',
                'Period': '202407',
                'Year': '2024',
                'Source': 'Manual Entry'
            }
            
            template_df = pd.concat([template_df, pd.DataFrame([sample_row])], ignore_index=True)
            
            template_df.to_excel(writer, sheet_name='Input Template', index=False)
            
            # 스타일 적용
            worksheet = writer.sheets['Input Template']
            self.base_reporter._apply_header_style(worksheet, len(template_df.columns))
            
            logger.info("입력 템플릿 시트 생성 완료")
            
        except ImportError:
            logger.warning("pandas가 설치되지 않음. 입력 템플릿 건너뜀")
        except Exception as e:
            logger.error(f"입력 템플릿 시트 생성 오류: {e}")
            
    def _create_csv_fallback(self, records: List, writer):
        """pandas 없이 CSV 형태로 데이터 생성"""
        try:
            # 간단한 텍스트 형태로 데이터 생성
            import csv
            import io
            
            output = io.StringIO()
            writer_csv = csv.writer(output)
            
            # 헤더
            writer_csv.writerow([
                'Date', 'Product Code', 'Product Description', 
                'Origin Country', 'Destination Country',
                'Trade Value (USD)', 'Quantity (kg)', 'Trade Type',
                'Period', 'Year', 'Source'
            ])
            
            # 데이터
            for record in records:
                writer_csv.writerow([
                    record.date, record.product_code, record.product_description,
                    record.country_origin, record.country_destination,
                    record.trade_value, record.quantity, record.trade_type,
                    record.period, record.year, record.source
                ])
            
            # 파일로 저장
            fallback_filename = f"reports/trade_data_fallback_{datetime.now().strftime('%Y%m%d')}.csv"
            with open(fallback_filename, 'w', newline='', encoding='utf-8') as f:
                f.write(output.getvalue())
                
            logger.info(f"CSV 폴백 파일 생성: {fallback_filename}")
            
        except Exception as e:
            logger.error(f"CSV 폴백 생성 오류: {e}")
