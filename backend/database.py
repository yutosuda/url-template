import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# データベースURL（環境変数から取得、デフォルトはローカルSQLite）
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")

# SQLiteの場合は追加設定
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        echo=True  # 開発時はSQLログを出力
    )
else:
    engine = create_engine(DATABASE_URL, echo=True)

# セッションファクトリー
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラス
Base = declarative_base()

# データベースセッションの依存性注入用
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 