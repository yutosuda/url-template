"""
Authentication API routes for URL shortener service.
"""
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import logging

import crud
import schemas
from database import get_db
from config import settings
from .exceptions import AuthenticationError

logger = logging.getLogger(__name__)

# Create authentication router
router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """アクセストークン作成"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """現在のユーザーを取得"""
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise AuthenticationError("トークンに有効なユーザー情報が含まれていません")
    except JWTError as e:
        raise AuthenticationError(
            "認証トークンが無効です",
            details={"jwt_error": str(e)} if settings.debug else None
        )
    
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise AuthenticationError(
            "ユーザーが見つかりません",
            details={"email": email} if settings.debug else None
        )
    return user


@router.post("/login", response_model=schemas.Token)
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """ユーザーログイン"""
    logger.info(f"Login attempt for email: {user.email}")
    
    db_user = crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        logger.warning(f"Failed login attempt for email: {user.email}")
        raise AuthenticationError(
            "メールアドレスまたはパスワードが間違っています",
            details={"email": user.email} if settings.debug else None
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    
    logger.info(f"Successful login for email: {user.email}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user
    }


@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """現在のユーザー情報取得"""
    logger.info(f"User info requested for: {current_user.email}")
    return current_user 