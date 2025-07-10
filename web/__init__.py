"""
Web 모듈 - Flask 애플리케이션의 모든 컴포넌트
"""

# 앱 설정
from .app_config import create_app, create_components

# API 핸들러들
from .data_api import DataAPIHandler
from .ai_api import AIAPIHandler
from .product_api import ProductAPIHandler
from .report_api import ReportAPIHandler
from .dashboard_api import DashboardAPI
from .telegram_api import TelegramAPI
from .database_api import DatabaseAPI
from .health_api import HealthAPI

__all__ = [
    'create_app',
    'create_components', 
    'DataAPIHandler',
    'AIAPIHandler',
    'ProductAPIHandler',
    'ReportAPIHandler',
    'DashboardAPI',
    'TelegramAPI',
    'DatabaseAPI',
    'HealthAPI'
]