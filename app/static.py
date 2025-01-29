from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

def setup_static_files(app: FastAPI):
    # Create uploads directory if it doesn't exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    # Mount the uploads directory
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") 