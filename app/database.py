from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
from sqlalchemy.exc import OperationalError

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@db/product_db"

def create_db_engine():
    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            engine = create_engine(
                SQLALCHEMY_DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            # Test the connection
            engine.connect()
            return engine
        except OperationalError as e:
            retry_count += 1
            if retry_count == max_retries:
                raise Exception(f"Failed to connect to database after {max_retries} attempts")
            print(f"Database connection attempt {retry_count} failed, retrying in 10 seconds...")
            time.sleep(10)

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 