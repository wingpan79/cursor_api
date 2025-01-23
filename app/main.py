from fastapi import FastAPI
from app.routes import category_routes, product_routes, product_image_routes
from app.database import engine
from app.models import category, product, product_image, api_log
from app.middleware.api_logger import APILoggerMiddleware

# Create database tables
#category.Base.metadata.create_all(bind=engine)
#product.Base.metadata.create_all(bind=engine)
#product_image.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add API Logger middleware
app.add_middleware(APILoggerMiddleware)

# Include routers
app.include_router(category_routes.router, tags=["categories"])
app.include_router(product_routes.router, tags=["products"])
app.include_router(product_image_routes.router, tags=["product_images"])

@app.get("/")
def read_root():
    return {"Hello": "World"} 