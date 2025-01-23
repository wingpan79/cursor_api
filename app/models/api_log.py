from sqlalchemy import Column, BigInteger, String, JSON, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class APILog(Base):
    __tablename__ = "api_logs"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    #user_id = Column(BigInteger, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    endpoint = Column(String(255), nullable=False, index=True)
    method = Column(String(10), nullable=False)
    request_headers = Column(JSON, nullable=True)
    request_body = Column(JSON, nullable=True)
    response_status = Column(BigInteger, nullable=False)
    response_body = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=False)
    user_agent = Column(String(255), nullable=True)
    execution_time = Column(Float, nullable=True, comment='in seconds')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 