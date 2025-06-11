#!/usr/bin/env python3
"""
管理者ユーザー作成スクリプト
事前定義されたアカウントを作成します。
"""

import sys
import os
from sqlalchemy.orm import Session

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
import models, crud
from schemas import UserCreate

def create_admin_user():
    """管理者ユーザーを作成"""
    # データベーステーブル作成
    models.Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # 管理者アカウント情報
        admin_email = "admin@example.com"
        admin_password = "admin123"
        
        # 既存ユーザーチェック
        existing_user = crud.get_user_by_email(db, email=admin_email)
        if existing_user:
            print(f"管理者ユーザー '{admin_email}' は既に存在します。")
            return
        
        # 管理者ユーザー作成
        admin_user_data = UserCreate(
            email=admin_email,
            password=admin_password
        )
        
        admin_user = crud.create_user(db=db, user=admin_user_data)
        
        print(f"管理者ユーザーが作成されました:")
        print(f"  メールアドレス: {admin_user.email}")
        print(f"  パスワード: {admin_password}")
        print(f"  ID: {admin_user.id}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user() 