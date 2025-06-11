from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from api.routes import router
from config import settings
from utils.logging import setup_logging

# ログ設定
logger = setup_logging()

# データベーステーブルを作成
Base.metadata.create_all(bind=engine)

# FastAPIアプリケーションの初期化
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins + [
        "http://localhost:3001", 
        "http://frontend:3001"
    ],
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# ルートの登録
app.include_router(router)

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {"message": settings.api_title, "version": settings.api_version}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 