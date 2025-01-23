from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, Category as CategorySchema, CategoryBulkUpdate
from app.utils.text_processor import encode_description

router = APIRouter()

@router.post("/categories/", response_model=CategorySchema)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    print(category)
    # Encode the description before saving
    category_data = category.dict()
    #category_data['description'] = encode_description(category_data.get('description'))
    print(category_data)
    db_category = Category(**category_data)
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
    
    # Encode the description before updating
    update_data = category.dict(exclude_unset=True)
   # update_data['description'] = encode_description(update_data.get('description'))
    
    for key, value in update_data.items():
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
        
        # Encode the description before updating
        update_data = category_update.dict(exclude={'id'})
        update_data['description'] = encode_description(update_data.get('description'))
        
        for key, value in update_data.items():
            setattr(db_category, key, value)
        
        updated_categories.append(db_category)
    
    db.commit()
    for category in updated_categories:
        db.refresh(category)
    
    return updated_categories 