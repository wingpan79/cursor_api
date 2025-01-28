from datetime import datetime, timedelta
from jose import JWTError,jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.token import Token as TokenModel
from app.models.user import User as UserModel
from passlib.context import CryptContext
from typing import Annotated
from app.schemas.token import TokenData

#from dotenv import load_dotenv

#load_dotenv()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session = Depends(lambda: SessionLocal())):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
       
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        user = get_user(db, username=token_data.username)
    except JWTError:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    #if current_user.disabled:
        #raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def create_access_token(data: Annotated[dict, Depends()]):
    """Create a new access token."""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    #encoded_jwt = "test"

    # Store token in database
    db = SessionLocal()
    db_token = TokenModel(
        username=data["sub"],
        access_token=encoded_jwt,
        expires_at=expire
    )
    db.add(db_token)
    db.commit()
    db.close()
    
    return encoded_jwt

def verify_token(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(lambda: SessionLocal())):
    """Verify the token and return user_id if valid."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Verify JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        # Check if token exists in database and is not expired
        db_token = (
            db.query(TokenModel)
            .filter(TokenModel.access_token == token)
            .filter(TokenModel.expires_at > datetime.now())
            .first()
        )
        if not db_token:
            raise credentials_exception
            
        return username
    except JWTError:
        raise credentials_exception
    finally:
        db.close()