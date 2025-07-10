from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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

class DatabaseManager:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_record(self, record_data):
        record = TradeRecord(**record_data)
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
    
    def get_records_by_date_range(self, start_date, end_date):
        """날짜 범위로 레코드 조회"""
        return self.session.query(TradeRecord).filter(
            TradeRecord.created_at >= start_date,
            TradeRecord.created_at <= end_date
        ).all()
