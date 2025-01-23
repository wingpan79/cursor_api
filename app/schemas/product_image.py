from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductImageBase(BaseModel):
    image_path: str
    is_primary: bool = False

class ProductImageCreate(ProductImageBase):
    pass

class ProductImage(ProductImageBase):
    id: int
    product_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True 