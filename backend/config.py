"""
Configuration management for the URL shortener backend.
"""
import os
from typing import Optional, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # データベース設定
    database_url: str = "sqlite:///./url_shortener.db"
    
    # アプリケーション設定
    app_name: str = "URL短縮サービス"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # CORS設定 - 本番環境のドメインを追加
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://frontend:3000",  # Docker環境用
        "https://url-click-manager.xvps.jp",  # 本番環境
        "http://url-click-manager.xvps.jp"   # 本番環境（HTTP）
    ]
    
    # CORS許可メソッド（セキュリティ強化：必要なメソッドのみ許可）
    cors_methods: List[str] = [
        "GET",
        "POST", 
        "DELETE",
        "OPTIONS"  # プリフライトリクエスト用
    ]
    
    # CORS許可ヘッダー（セキュリティ強化：必要なヘッダーのみ許可）
    cors_headers: List[str] = [
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",  # JWT認証用
        "X-Requested-With"  # AJAX識別用
    ]
    
    # URL短縮設定 - 環境変数対応
    base_url: str = os.getenv("BASE_URL", "http://localhost:8000")
    short_code_length: int = 8
    
    # JWT認証設定
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # セキュリティ設定
    bcrypt_rounds: int = 12
    
    # ページネーション設定
    default_page_size: int = 20
    max_page_size: int = 100
    
    # ログ設定
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 環境変数から設定を読み込み
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 設定インスタンス
settings = Settings()

# 開発環境での設定上書き
if os.getenv("ENVIRONMENT") == "development":
    settings.debug = True
    settings.log_level = "DEBUG"

# 本番環境での設定上書き
if os.getenv("ENVIRONMENT") == "production":
    settings.debug = False
    settings.log_level = "WARNING"
    # 本番環境では必ず環境変数からシークレットキーを取得
    if os.getenv("SECRET_KEY"):
        settings.secret_key = os.getenv("SECRET_KEY")
    else:
        raise ValueError("本番環境ではSECRET_KEY環境変数の設定が必要です")
    
    # 本番環境でのbase_url自動設定
    if not os.getenv("BASE_URL"):
        settings.base_url = "https://url-click-manager.xvps.jp" 