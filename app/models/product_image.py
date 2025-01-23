from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'), index=True)
    image_path = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    product = relationship("Product", back_populates="images") 