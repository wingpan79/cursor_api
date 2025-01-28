from sqlalchemy import Column, String,  DateTime, Integer
from app.database import Base
from datetime import datetime
from sqlalchemy.sql import func


class Token(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    access_token = Column(String(500), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())