# Import required FastAPI components
from fastapi import APIRouter
# Create API router instance
import app.auth as auth
from app.models.token import Token as TokenModel
from app.schemas.token import Token 
from app.schemas.user import User as UserSchema, UserCreate, UserLogin
from app.models.user import User as UserModel
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from sqlalchemy.sql import func
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter()

@router.post("/register", response_model=UserSchema)
async def register_user(user: UserCreate, db: Session = Depends(get_db))->UserSchema:
    """Register a new user."""
    # Check if username already exists
    if db.query(UserModel).filter(UserModel.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists
    if db.query(UserModel).filter(UserModel.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = auth.get_password_hash(user.password)
    db_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(
    form_data: UserLogin,
    db: Session = Depends(get_db)
)->Token:
    """Login user and return access token."""
    # Authenticate user
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check for existing valid token
    existing_token = (
        db.query(TokenModel)
        .filter(TokenModel.username == user.username)
        .filter(TokenModel.expires_at > func.now())
        .first()
    )
    
    if existing_token:
        return {"access_token": existing_token.access_token, "token_type": "bearer"}
    
    # Create new token
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: Session = Depends(get_db)) -> Token:
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #access_token_expires = timedelta(minutes=240)
    access_token = auth.create_access_token(
        data={"sub": user.username}
    )
    return Token(access_token=access_token, token_type="bearer")