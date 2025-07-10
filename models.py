from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

Base = declarative_base()

class TradeRecord(Base):
    __tablename__ = 'trade_records'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    country_origin = Column(String(100), nullable=False)
    country_destination = Column(String(100), nullable=False)
    company_exporter = Column(String(200))
    company_importer = Column(String(200))
    product_code = Column(String(20), nullable=False)
    product_description = Column(String(500))
    quantity = Column(Float)
    unit = Column(String(20))
    value_usd = Column(Float, nullable=False)
    trade_type = Column(String(10), nullable=False)  # 'export' or 'import'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 상세 정보를 JSON으로 저장하는 필드 추가
    detailed_info = Column(Text)  # JSON 형태로 상세 정보 저장
    
    def set_detailed_info(self, info_dict):
        """상세 정보를 JSON으로 설정"""
        if info_dict:
            self.detailed_info = json.dumps(info_dict, ensure_ascii=False, default=str)
    
    def get_detailed_info(self):
        """상세 정보를 딕셔너리로 반환"""
        if self.detailed_info:
            try:
                return json.loads(self.detailed_info)
            except json.JSONDecodeError:
                return {}
        return {}

class DatabaseManager:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_record(self, record_data):
        # 기본 필드와 상세 정보 분리
        basic_fields = {
            'date', 'country_origin', 'country_destination', 
            'company_exporter', 'company_importer', 'product_code', 
            'product_description', 'quantity', 'unit', 'value_usd', 'trade_type'
        }
        
        basic_data = {k: v for k, v in record_data.items() if k in basic_fields}
        detailed_data = {k: v for k, v in record_data.items() if k not in basic_fields}
        
        record = TradeRecord(**basic_data)
        
        # 상세 정보가 있으면 JSON으로 저장
        if detailed_data:
            record.set_detailed_info(detailed_data)
        
        self.session.add(record)
        self.session.commit()
        return record
    
    def save_record(self, record_data):
        """add_record의 별칭 - 호환성을 위해"""
        return self.add_record(record_data)
    
    def get_latest_records(self, days=7):
        from datetime import datetime, timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        return self.session.query(TradeRecord).filter(
            TradeRecord.created_at >= cutoff_date
        ).all()
    
    def get_recent_records(self, limit=10):
        """최근 레코드 조회"""
        return self.session.query(TradeRecord).order_by(
            TradeRecord.created_at.desc()
        ).limit(limit).all()
    
    def get_records_by_date_range(self, start_date, end_date):
        """날짜 범위로 레코드 조회"""
        return self.session.query(TradeRecord).filter(
            TradeRecord.created_at >= start_date,
            TradeRecord.created_at <= end_date
        ).all()

    def get_detailed_record(self, record_id):
        """ID로 상세 레코드 조회"""
        record = self.session.query(TradeRecord).filter(
            TradeRecord.id == record_id
        ).first()
        
        if record:
            # 기본 정보와 상세 정보를 합쳐서 반환
            result = {
                'id': record.id,
                'date': record.date,
                'country_origin': record.country_origin,
                'country_destination': record.country_destination,
                'company_exporter': record.company_exporter,
                'company_importer': record.company_importer,
                'product_code': record.product_code,
                'product_description': record.product_description,
                'quantity': record.quantity,
                'unit': record.unit,
                'value_usd': record.value_usd,
                'trade_type': record.trade_type,
                'created_at': record.created_at
            }
            
            # 상세 정보 추가
            detailed_info = record.get_detailed_info()
            result.update(detailed_info)
            
            return result
        
        return None

    def close(self):
        """세션 종료"""
        self.session.close()
