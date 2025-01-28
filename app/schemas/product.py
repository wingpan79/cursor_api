from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class ProductBase(BaseModel):
    category_id: Optional[int]=None
    name: str
    sku: str
    description: Optional[str] = None
    price: Decimal
    stock: int
    status: str = "active"

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    category_id: Optional[int] = None
    name: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    status: Optional[str] = None

# Add this new schema for bulk updates
class ProductBulkUpdate(ProductBase):
    id: int


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True 