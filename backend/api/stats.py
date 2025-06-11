"""
Statistics API routes for URL shortener service.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pytz
import logging

import crud
import schemas
from database import get_db
from config import settings
from .auth import get_current_user
from .exceptions import DatabaseError

logger = logging.getLogger(__name__)

# Create statistics router
router = APIRouter(prefix="/stats", tags=["statistics"])

# 日本のタイムゾーン
JST = pytz.timezone('Asia/Tokyo')


def convert_to_jst(utc_datetime):
    """UTC時刻をJST時刻に変換する"""
    if utc_datetime.tzinfo is None:
        # タイムゾーン情報がない場合はUTCとして扱う
        utc_datetime = pytz.utc.localize(utc_datetime)
    return utc_datetime.astimezone(JST)


@router.get("", response_model=schemas.URLStats)
async def get_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """統計情報取得（認証必須）"""
    logger.info(f"Fetching application statistics for user: {current_user.email}")
    
    try:
        total_urls = crud.get_url_count(db)
        total_clicks = crud.get_total_clicks(db)
        top_urls_data = crud.get_top_urls(db, limit=5)
        
        # トップURLのレスポンス形式に変換
        top_urls = []
        for url in top_urls_data:
            short_url = f"{settings.base_url}/{url.short_code}"
            top_urls.append(schemas.URLResponse(
                id=url.id,
                original_url=url.original_url,
                short_code=url.short_code,
                click_count=url.click_count,
                created_at=convert_to_jst(url.created_at),
                short_url=short_url
            ))
        
        stats_result = schemas.URLStats(
            total_urls=total_urls,
            total_clicks=total_clicks,
            top_urls=top_urls
        )
        
        logger.info(f"Statistics retrieved successfully for user: {current_user.email} - URLs: {total_urls}, Clicks: {total_clicks}")
        return stats_result
    except Exception as e:
        logger.error(f"Error fetching stats for user: {current_user.email} - {str(e)}")
        raise DatabaseError(
            "統計情報取得中にエラーが発生しました",
            details={"original_error": str(e)} if settings.debug else None
        ) 