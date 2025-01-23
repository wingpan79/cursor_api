from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"

class CategoryCreate(CategoryBase):
    pass

# Add this new schema for bulk updates
class CategoryBulkUpdate(CategoryBase):
    id: int

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True 