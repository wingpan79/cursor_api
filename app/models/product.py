from sqlalchemy import Column, String, Text, Enum, DateTime, BigInteger, ForeignKey, Numeric, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    category_id = Column(BigInteger, ForeignKey('categories.id', ondelete='SET NULL'), index=True)
    name = Column(String(255), nullable=False, index=True)
    sku = Column(String(50), unique=True, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10,2), nullable=False, default=0.00)
    stock = Column(Integer, nullable=False, default=0)
    status = Column(Enum('active', 'inactive'), default='active', index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan") 