from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field, EmailStr

# 認証関連のスキーマ
class UserCreate(BaseModel):
    """ユーザー登録用スキーマ"""
    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., min_length=6, description="パスワード（6文字以上）")

class UserLogin(BaseModel):
    """ユーザーログイン用スキーマ"""
    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., description="パスワード")

class UserResponse(BaseModel):
    """ユーザー応答用スキーマ"""
    id: int
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """トークン応答用スキーマ"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# URL関連のスキーマ
class URLCreate(BaseModel):
    """URL作成用スキーマ"""
    original_url: HttpUrl = Field(..., description="短縮したい元のURL")

class URLResponse(BaseModel):
    """URL応答用スキーマ"""
    id: int
    original_url: str
    short_code: str
    click_count: int
    created_at: datetime
    short_url: str = Field(..., description="完全な短縮URL")
    
    class Config:
        from_attributes = True

class URLList(BaseModel):
    """URL一覧用スキーマ"""
    urls: List[URLResponse]
    total: int

# クリック関連のスキーマ
class ClickCreate(BaseModel):
    """クリック記録用スキーマ"""
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    referrer: Optional[str] = None

class ClickResponse(BaseModel):
    """クリック応答用スキーマ"""
    id: int
    url_id: int
    clicked_at: datetime
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    referrer: Optional[str] = None
    
    class Config:
        from_attributes = True

# エラー応答用スキーマ
class ErrorResponse(BaseModel):
    """エラー応答用スキーマ"""
    detail: str
    error_code: Optional[str] = None

# 統計情報用スキーマ
class URLStats(BaseModel):
    """URL統計情報用スキーマ"""
    total_urls: int
    total_clicks: int
    top_urls: List[URLResponse] 