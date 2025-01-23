from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.product_image import ProductImage
from app.schemas.product_image import ProductImageCreate, ProductImage as ProductImageSchema

router = APIRouter()

@router.post("/products/{product_id}/images/", response_model=ProductImageSchema)
def create_product_image(
    product_id: int,
    image: ProductImageCreate,
    db: Session = Depends(get_db)
):
    db_image = ProductImage(**image.dict(), product_id=product_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

@router.get("/products/{product_id}/images/", response_model=List[ProductImageSchema])
def read_product_images(product_id: int, db: Session = Depends(get_db)):
    images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
    return images

@router.delete("/products/images/{image_id}")
def delete_product_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    
    db.delete(db_image)
    db.commit()
    return {"message": "Image deleted successfully"}

@router.put("/products/images/{image_id}/set-primary", response_model=ProductImageSchema)
def set_primary_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Reset all images for this product to non-primary
    db.query(ProductImage).filter(
        ProductImage.product_id == db_image.product_id
    ).update({"is_primary": False})
    
    # Set the selected image as primary
    db_image.is_primary = True
    db.commit()
    db.refresh(db_image)
    return db_image 