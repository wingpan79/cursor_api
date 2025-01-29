from fastapi import FastAPI
from app.routes import category_routes, product_routes, product_image_routes,token_routes
from app.middleware.api_logger import APILoggerMiddleware
from app.static import setup_static_files


# Create database tables
#category.Base.metadata.create_all(bind=engine)
#product.Base.metadata.create_all(bind=engine)
#token.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add API Logger middleware
app.add_middleware(APILoggerMiddleware)

# Setup static file serving
setup_static_files(app)

# Include routers
app.include_router(category_routes.router, tags=["categories"])
app.include_router(product_routes.router, tags=["products"])
app.include_router(product_image_routes.router, tags=["product_images"])
app.include_router(token_routes.router, tags=["tokens"])

@app.get("/")
def read_root():
    return {"Hello": "World"} 