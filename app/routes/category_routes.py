from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, Category as CategorySchema, CategoryBulkUpdate

router = APIRouter()

@router.post("/categories/", response_model=CategorySchema)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/categories/", response_model=List[CategorySchema])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories

@router.get("/categories/{category_id}", response_model=CategorySchema)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/categories/{category_id}", response_model=CategorySchema)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/categories/bulk", response_model=List[CategorySchema])
def bulk_update_categories(categories: List[CategoryBulkUpdate], db: Session = Depends(get_db)):
    updated_categories = []
    
    for category_update in categories:
        db_category = db.query(Category).filter(Category.id == category_update.id).first()
        if db_category is None:
            raise HTTPException(
                status_code=404, 
                detail=f"Category with id {category_update.id} not found"
            )
        
        # Update category attributes
        for key, value in category_update.dict(exclude={'id'}).items():
            setattr(db_category, key, value)
        
        updated_categories.append(db_category)
    
    db.commit()
    # Refresh all updated categories
    for category in updated_categories:
        db.refresh(category)
    
    return updated_categories 