"""
차트 생성기 - 보고서용 차트 및 그래프 생성
"""
import logging
from datetime import datetime, timedelta
from typing import List, Dict
from .base_reporter import BaseReporter

logger = logging.getLogger(__name__)

class ChartGenerator:
    """차트 생성 클래스"""
    
    def __init__(self, base_reporter: BaseReporter):
        self.base_reporter = base_reporter
        
    def create_charts(self, records: List, writer):
        """기본 차트 생성"""
        try:
            # matplotlib가 설치된 경우에만 차트 생성
            import matplotlib.pyplot as plt
            import pandas as pd
            
            # 데이터프레임 생성
            df = self.base_reporter._create_dataframe_from_records(records)
            
            # 국가별 무역량 파이 차트
            self._create_country_pie_chart(df)
            
            # 월별 트렌드 라인 차트  
            self._create_monthly_trend_chart(df)
            
            logger.info("차트 생성 완료")
            
        except ImportError:
            logger.warning("matplotlib/pandas가 설치되지 않음. 차트 생성 건너뜀")
        except Exception as e:
            logger.error(f"차트 생성 오류: {e}")
            
    def create_weekly_charts(self, records: List, writer):
        """주간 차트 생성"""
        try:
            import matplotlib.pyplot as plt
            import pandas as pd
            
            df = self.base_reporter._create_dataframe_from_records(records)
            
            # 주간 일별 트렌드
            self._create_daily_trend_chart(df, "weekly")
            
            logger.info("주간 차트 생성 완료")
            
        except ImportError:
            logger.warning("차트 라이브러리 없음")
        except Exception as e:
            logger.error(f"주간 차트 생성 오류: {e}")
            
    def create_monthly_charts(self, records: List, writer):
        """월간 차트 생성"""
        try:
            import matplotlib.pyplot as plt
            import pandas as pd
            
            df = self.base_reporter._create_dataframe_from_records(records)
            
            # 월간 주별 트렌드
            self._create_weekly_trend_chart(df)
            
            # 제품별 비교 차트
            self._create_product_comparison_chart(df)
            
            logger.info("월간 차트 생성 완료")
            
        except ImportError:
            logger.warning("차트 라이브러리 없음")
        except Exception as e:
            logger.error(f"월간 차트 생성 오류: {e}")
            
    def create_custom_charts(self, records: List, writer, start_date: datetime, end_date: datetime):
        """사용자 정의 차트 생성"""
        try:
            import matplotlib.pyplot as plt
            import pandas as pd
            
            df = self.base_reporter._create_dataframe_from_records(records)
            
            # 기간별 트렌드 차트
            self._create_period_trend_chart(df, start_date, end_date)
            
            logger.info("사용자 정의 차트 생성 완료")
            
        except ImportError:
            logger.warning("차트 라이브러리 없음")
        except Exception as e:
            logger.error(f"사용자 정의 차트 생성 오류: {e}")
            
    def _create_country_pie_chart(self, df):
        """국가별 무역량 파이 차트"""
        try:
            import matplotlib.pyplot as plt
            
            country_data = df.groupby('Origin Country')['Trade Value (USD)'].sum()
            
            plt.figure(figsize=(10, 8))
            plt.pie(country_data.values, labels=country_data.index, autopct='%1.1f%%')
            plt.title('Trade Value by Origin Country')
            plt.savefig('reports/country_pie_chart.png', dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            logger.error(f"국가별 파이 차트 생성 오류: {e}")
            
    def _create_monthly_trend_chart(self, df):
        """월별 트렌드 라인 차트"""
        try:
            import matplotlib.pyplot as plt
            import pandas as pd
            
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month'] = df['Date'].dt.to_period('M')
            
            monthly_data = df.groupby('Month')['Trade Value (USD)'].sum()
            
            plt.figure(figsize=(12, 6))
            plt.plot(monthly_data.index.astype(str), monthly_data.values, marker='o')
            plt.title('Monthly Trade Value Trend')
            plt.xlabel('Month')
            plt.ylabel('Trade Value (USD)')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.savefig('reports/monthly_trend_chart.png', dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            logger.error(f"월별 트렌드 차트 생성 오류: {e}")
            
    def _create_daily_trend_chart(self, df, period_type: str):
        """일별 트렌드 차트"""
        try:
            import matplotlib.pyplot as plt
            import pandas as pd
            
            df['Date'] = pd.to_datetime(df['Date'])
            daily_data = df.groupby('Date')['Trade Value (USD)'].sum()
            
            plt.figure(figsize=(12, 6))
            plt.plot(daily_data.index, daily_data.values, marker='o')
            plt.title(f'{period_type.title()} Daily Trade Value Trend')
            plt.xlabel('Date')
            plt.ylabel('Trade Value (USD)')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.savefig(f'reports/{period_type}_daily_trend_chart.png', dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            logger.error(f"일별 트렌드 차트 생성 오류: {e}")
            
    def _create_weekly_trend_chart(self, df):
        """주별 트렌드 차트"""
        try:
            import matplotlib.pyplot as plt
            import pandas as pd
            
            df['Date'] = pd.to_datetime(df['Date'])
            df['Week'] = df['Date'].dt.to_period('W')
            
            weekly_data = df.groupby('Week')['Trade Value (USD)'].sum()
            
            plt.figure(figsize=(12, 6))
            plt.plot(weekly_data.index.astype(str), weekly_data.values, marker='o')
            plt.title('Weekly Trade Value Trend')
            plt.xlabel('Week')
            plt.ylabel('Trade Value (USD)')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.savefig('reports/weekly_trend_chart.png', dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            logger.error(f"주별 트렌드 차트 생성 오류: {e}")
            
    def _create_product_comparison_chart(self, df):
        """제품별 비교 차트"""
        try:
            import matplotlib.pyplot as plt
            
            product_data = df.groupby('Product Code')['Trade Value (USD)'].sum()
            
            plt.figure(figsize=(12, 6))
            plt.bar(product_data.index, product_data.values)
            plt.title('Trade Value by Product Code')
            plt.xlabel('Product Code')
            plt.ylabel('Trade Value (USD)')
            plt.xticks(rotation=45)
            plt.grid(True, axis='y')
            plt.savefig('reports/product_comparison_chart.png', dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            logger.error(f"제품별 비교 차트 생성 오류: {e}")
            
    def _create_period_trend_chart(self, df, start_date: datetime, end_date: datetime):
        """기간별 트렌드 차트"""
        try:
            import matplotlib.pyplot as plt
            import pandas as pd
            
            df['Date'] = pd.to_datetime(df['Date'])
            
            # 기간에 따라 그룹화 단위 결정
            days_diff = (end_date - start_date).days
            
            if days_diff <= 7:
                # 7일 이하: 일별
                period_data = df.groupby('Date')['Trade Value (USD)'].sum()
                title = 'Daily Trade Value Trend'
            elif days_diff <= 60:
                # 60일 이하: 주별
                df['Week'] = df['Date'].dt.to_period('W')
                period_data = df.groupby('Week')['Trade Value (USD)'].sum()
                title = 'Weekly Trade Value Trend'
            else:
                # 60일 초과: 월별
                df['Month'] = df['Date'].dt.to_period('M')
                period_data = df.groupby('Month')['Trade Value (USD)'].sum()
                title = 'Monthly Trade Value Trend'
            
            plt.figure(figsize=(12, 6))
            plt.plot(period_data.index.astype(str), period_data.values, marker='o')
            plt.title(title)
            plt.xlabel('Period')
            plt.ylabel('Trade Value (USD)')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.savefig('reports/custom_period_trend_chart.png', dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            logger.error(f"기간별 트렌드 차트 생성 오류: {e}")
