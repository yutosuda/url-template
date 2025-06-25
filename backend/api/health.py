"""
Health check endpoints for monitoring service status.
Provides comprehensive health monitoring including database connectivity.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import pytz
import os

from database import get_db
from config import settings

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    包括的ヘルスチェックエンドポイント
    
    - サービス稼働状況
    - データベース接続確認
    - 基本設定確認
    
    Returns:
        dict: ヘルスチェック結果
    """
    try:
        # データベース接続テスト
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # 現在時刻（JST）
    jst = pytz.timezone('Asia/Tokyo')
    current_time = datetime.now(jst).isoformat()
    
    health_data = {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "timestamp": current_time,
        "service": {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": os.getenv("ENVIRONMENT", "unknown")
        },
        "database": {
            "status": db_status,
            "type": "SQLite"
        },
        "uptime": "running"
    }
    
    # データベースが不健全な場合は503エラーを返す
    if db_status != "healthy":
        raise HTTPException(status_code=503, detail=health_data)
    
    return health_data

@router.get("/health/simple")
async def simple_health_check():
    """
    シンプルなヘルスチェックエンドポイント
    データベース接続を確認せず、サービスの基本稼働状況のみ確認
    
    Returns:
        dict: 基本ヘルスチェック結果
    """
    jst = pytz.timezone('Asia/Tokyo')
    current_time = datetime.now(jst).isoformat()
    
    return {
        "status": "healthy",
        "timestamp": current_time,
        "service": settings.app_name,
        "version": settings.app_version
    }

@router.get("/health/database")
async def database_health_check(db: Session = Depends(get_db)):
    """
    データベース専用ヘルスチェックエンドポイント
    
    Returns:
        dict: データベース接続状況
    """
    try:
        # より詳細なデータベーステスト
        result = db.execute(text("SELECT COUNT(*) as count FROM sqlite_master WHERE type='table'"))
        table_count = result.scalar()
        
        db_info = {
            "status": "healthy",
            "connection": "active",
            "tables_count": table_count,
            "database_file": settings.database_url
        }
        
        return {
            "database": db_info,
            "timestamp": datetime.now(pytz.timezone('Asia/Tokyo')).isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=503, 
            detail={
                "database": {
                    "status": "unhealthy",
                    "error": str(e)
                },
                "timestamp": datetime.now(pytz.timezone('Asia/Tokyo')).isoformat()
            }
        ) 