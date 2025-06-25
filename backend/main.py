from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from database import engine, Base
from api.routes import router
from config import settings

# 統一エラーハンドリングのインポート
from api.exceptions import (
    BaseAPIException,
    base_api_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)

# データベーステーブルを作成
Base.metadata.create_all(bind=engine)

# FastAPIアプリケーションの初期化
app = FastAPI(
    title=settings.app_name,
    description="URL短縮サービスAPI",
    version=settings.app_version
)

# CORS設定（セキュリティ強化：必要な設定のみ許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# 統一エラーハンドラーの登録
app.add_exception_handler(BaseAPIException, base_api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# ルートの登録（APIプレフィックス付き）
app.include_router(router, prefix="/api")

# リダイレクト機能を個別に登録（プレフィックスなし）
from api.redirect import router as redirect_router
app.include_router(redirect_router)

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {"message": settings.app_name, "version": settings.app_version}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 