# Import required FastAPI components
from fastapi import APIRouter, Depends, HTTPException
# Import SQLAlchemy session management
from sqlalchemy.orm import Session
# Import for raw SQL queries
from sqlalchemy import text
# Import typing for type hints
from typing import List
# Import database connection utility
from app.database import get_db
# Import Product model
from app.models.product import Product
# Import Product-related schemas
from app.schemas.product import ProductCreate, Product as ProductSchema, ProductBulkUpdate

# Create API router instance
router = APIRouter()

# Endpoint to create a single product
@router.post("/products/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Create new Product instance from request data
    db_product = Product(**product.dict())
    # Add product to database session
    db.add(db_product)
    # Commit the transaction
    db.commit()
    # Refresh the product instance to get updated data (like id)
    db.refresh(db_product)
    return db_product

# Endpoint to create multiple products in one request
@router.post("/products/bulk", response_model=List[ProductSchema])
def bulk_create_products(products: List[ProductCreate], db: Session = Depends(get_db)):
    # Create list of Product instances from request data
    db_products = [Product(**product.dict()) for product in products]
    # Add all products to database session
    db.add_all(db_products)
    # Commit the transaction
    db.commit()
    # Refresh all product instances
    for product in db_products:
        db.refresh(product)
    return db_products

# Endpoint to get list of products with pagination
@router.get("/products/", response_model=List[ProductSchema])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Example of raw SQL query (commented out ORM version)
    #products = db.query(Product).offset(skip).limit(limit).all()
    # Execute raw SQL query
    products = db.execute(text("SELECT * FROM products"))
    # Convert result to dictionary format
    products = products.mappings().all()
    # Debug print
    print(products)
    return products

# Endpoint to get a single product by ID
@router.get("/products/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    # Query database for product with specific ID
    product = db.query(Product).filter(Product.id == product_id).first()
    # Raise 404 if product not found
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Endpoint to update a single product
@router.put("/products/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    # Find product in database
    db_product = db.query(Product).filter(Product.id == product_id).first()
    # Raise 404 if product not found
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    #update_data = product.dict(exclude_unset=True)
    # Update all fields from request data
    #print(product.dict())
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    # Commit changes
    db.commit()
    # Refresh product instance
    db.refresh(db_product)
    return db_product

# Endpoint to delete a product
@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # Find product in database
    db_product = db.query(Product).filter(Product.id == product_id).first()
    # Raise 404 if product not found
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Delete product
    db.delete(db_product)
    # Commit changes
    db.commit()
    return {"message": "Product deleted successfully"}

# Endpoint to update multiple products in one request
@router.put("/products/bulk", response_model=List[ProductSchema])
def bulk_update_products(products: List[ProductBulkUpdate], db: Session = Depends(get_db)):
    # List to store updated products
    updated_products = []
    
    # Process each product update request
    for product_update in products:
        # Find product in database
        db_product = db.query(Product).filter(Product.id == product_update.id).first()
        # Raise 404 if product not found
        if db_product is None:
            raise HTTPException(
                status_code=404, 
                detail=f"Product with id {product_update.id} not found"
            )
        
        # Update product attributes excluding ID
        for key, value in product_update.dict(exclude={'id'}).items():
            setattr(db_product, key, value)
        
        # Add to list of updated products
        updated_products.append(db_product)
    
    # Commit all changes in one transaction
    db.commit()
    # Refresh all updated products
    for product in updated_products:
        db.refresh(product)
    
    return updated_products 