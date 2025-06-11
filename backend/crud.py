import secrets
import string
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from models import URL, Click, User
from schemas import URLCreate, ClickCreate, UserCreate
from passlib.context import CryptContext

# パスワードハッシュ化設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワード検証"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """パスワードハッシュ化"""
    return pwd_context.hash(password)

# ユーザー関連のCRUD操作
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """メールアドレスでユーザーを取得"""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """ユーザー作成"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """ユーザー認証"""
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def generate_short_code(length: int = 8) -> str:
    """短縮コードを生成する"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def get_unique_short_code(db: Session, length: int = 8) -> str:
    """重複しない短縮コードを生成する"""
    while True:
        short_code = generate_short_code(length)
        if not get_url_by_short_code(db, short_code):
            return short_code

# URL関連のCRUD操作
def create_url(db: Session, url_create: URLCreate) -> URL:
    """新しいURLを作成する"""
    short_code = get_unique_short_code(db)
    db_url = URL(
        original_url=str(url_create.original_url),
        short_code=short_code
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url_by_short_code(db: Session, short_code: str) -> Optional[URL]:
    """短縮コードでURLを取得する"""
    return db.query(URL).filter(URL.short_code == short_code).first()

def get_url_by_id(db: Session, url_id: int) -> Optional[URL]:
    """IDでURLを取得する"""
    return db.query(URL).filter(URL.id == url_id).first()

def get_urls(db: Session, skip: int = 0, limit: int = 100) -> List[URL]:
    """URL一覧を取得する"""
    return db.query(URL).order_by(desc(URL.created_at)).offset(skip).limit(limit).all()

def get_urls_count(db: Session) -> int:
    """URL総数を取得する"""
    return db.query(URL).count()

def delete_url(db: Session, url_id: int) -> bool:
    """URLを削除する（関連するクリックも削除）"""
    # 関連するクリックを先に削除
    db.query(Click).filter(Click.url_id == url_id).delete()
    
    # URLを削除
    url = get_url_by_id(db, url_id)
    if url:
        db.delete(url)
        db.commit()
        return True
    return False

def increment_click_count(db: Session, url_id: int) -> bool:
    """クリック数をインクリメントする"""
    url = get_url_by_id(db, url_id)
    if url:
        url.click_count += 1
        db.commit()
        return True
    return False

# クリック関連のCRUD操作
def create_click(db: Session, url_id: int, click_data: ClickCreate) -> Click:
    """新しいクリックを記録する"""
    db_click = Click(
        url_id=url_id,
        user_agent=click_data.user_agent,
        ip_address=click_data.ip_address,
        referrer=click_data.referrer
    )
    db.add(db_click)
    db.commit()
    db.refresh(db_click)
    return db_click

def get_clicks_by_url(db: Session, url_id: int, skip: int = 0, limit: int = 100) -> List[Click]:
    """特定URLのクリック履歴を取得する"""
    return db.query(Click).filter(Click.url_id == url_id).order_by(desc(Click.clicked_at)).offset(skip).limit(limit).all()

# 統計関連の操作
def get_total_clicks(db: Session) -> int:
    """総クリック数を取得する"""
    return db.query(Click).count()

def get_top_urls(db: Session, limit: int = 10) -> List[URL]:
    """クリック数上位のURLを取得する"""
    return db.query(URL).order_by(desc(URL.click_count)).limit(limit).all() 