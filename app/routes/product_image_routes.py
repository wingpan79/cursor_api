from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime
from app.database import get_db
from app.models.product_image import ProductImage
from app.schemas.product_image import ProductImageCreate, ProductImage as ProductImageSchema
from app.models.product import Product

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/products/{product_id}/images/", response_model=ProductImageSchema)
async def create_product_image(
    product_id: int,
    image: ProductImageCreate,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Check if product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Create unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #get the file extension eg .jpg, .png, .jpeg
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"product_{product_id}_{timestamp}{file_extension}"
    
    # Create year/month based directory structure
    year_month = datetime.now().strftime("%Y/%m")
    upload_path = os.path.join(UPLOAD_DIR, year_month)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    
    # Full path for the file
    file_path = os.path.join(upload_path, unique_filename)
    
    try:
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")
    
    # Create database record
    relative_path = os.path.join(year_month, unique_filename)
    db_image = ProductImage(
        product_id=product_id,
        image_path=relative_path,
        is_primary=image.is_primary  # Set to True if it's the first image
    )
    
    # Check if this is the first image for the product
    #existing_images = db.query(ProductImage).filter(
    #    ProductImage.product_id == product_id
    #).count()
    #if existing_images == 0:
    #    db_image.is_primary = True
    
    try:
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
    except Exception as e:
        # Remove uploaded file if database operation fails
        if os.path.exists(file_path):
            os.remove(file_path)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create image record: {str(e)}")
    
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
    
    # Delete the physical file
    file_path = os.path.join(UPLOAD_DIR, db_image.image_path)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete file {file_path}: {str(e)}")
    
    # Delete database record
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