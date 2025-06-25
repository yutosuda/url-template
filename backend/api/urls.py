"""
URL management API routes for URL shortener service.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
import pytz
import logging

import crud
import schemas
from database import get_db
from config import settings
from .auth import get_current_user
from .exceptions import ValidationError, NotFoundError, DatabaseError

logger = logging.getLogger(__name__)

# Create URL management router
router = APIRouter(prefix="/urls", tags=["url-management"])

# 日本のタイムゾーン
JST = pytz.timezone('Asia/Tokyo')


def convert_to_jst(utc_datetime):
    """UTC時刻をJST時刻に変換する"""
    if utc_datetime.tzinfo is None:
        # タイムゾーン情報がない場合はUTCとして扱う
        utc_datetime = pytz.utc.localize(utc_datetime)
    return utc_datetime.astimezone(JST)


@router.post("", response_model=schemas.URLResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    url: schemas.URLCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """短縮URL作成（認証必須）"""
    logger.info(f"Creating URL: {url.original_url} for user: {current_user.email}")
    
    # 基本的なURL検証
    url_str = str(url.original_url)
    if not url_str.startswith(('http://', 'https://')):
        logger.warning(f"Invalid URL format: {url.original_url}")
        raise ValidationError(
            "URLは http:// または https:// で始まる必要があります",
            details={"provided_url": url_str}
        )
    
    try:
        db_url = crud.create_url(db=db, url_create=url)
        
        # レスポンス用に短縮URLを生成（/r/プレフィックス付き）
        short_url = f"{settings.base_url}/r/{db_url.short_code}"
        
        response = schemas.URLResponse(
            id=db_url.id,
            original_url=db_url.original_url,
            short_code=db_url.short_code,
            click_count=db_url.click_count,
            created_at=convert_to_jst(db_url.created_at),
            short_url=short_url
        )
        
        logger.info(f"URL created successfully: {db_url.short_code} for user: {current_user.email}")
        return response
    except Exception as e:
        logger.error(f"Error creating URL: {str(e)} for user: {current_user.email}")
        raise DatabaseError(
            "URL作成中にエラーが発生しました",
            details={"original_error": str(e)} if settings.debug else None
        )


@router.get("", response_model=schemas.URLList)
async def get_urls(
    skip: int = 0, 
    limit: int = 20, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """URL一覧取得（認証必須）"""
    if limit > 100:
        limit = 100
    
    logger.info(f"Fetching URLs: skip={skip}, limit={limit} for user: {current_user.email}")
    
    try:
        urls = crud.get_urls(db, skip=skip, limit=limit)
        total = crud.get_urls_count(db)
        
        # レスポンス用にshort_urlを追加（/r/プレフィックス付き）
        url_responses = []
        for url in urls:
            short_url = f"{settings.base_url}/r/{url.short_code}"
            url_responses.append(schemas.URLResponse(
                id=url.id,
                original_url=url.original_url,
                short_code=url.short_code,
                click_count=url.click_count,
                created_at=convert_to_jst(url.created_at),
                short_url=short_url
            ))
        
        logger.info(f"Retrieved {len(url_responses)} URLs for user: {current_user.email}")
        return schemas.URLList(urls=url_responses, total=total)
    except Exception as e:
        logger.error(f"Error fetching URLs: {str(e)} for user: {current_user.email}")
        raise DatabaseError(
            "URL一覧取得中にエラーが発生しました",
            details={"original_error": str(e)} if settings.debug else None
        )


@router.delete("/{url_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_url(
    url_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """URL削除（認証必須）"""
    logger.info(f"Deleting URL: {url_id} for user: {current_user.email}")
    
    try:
        success = crud.delete_url(db=db, url_id=url_id)
        if not success:
            logger.warning(f"URL not found for deletion: {url_id} for user: {current_user.email}")
            raise NotFoundError(
                "指定されたURLが見つかりません",
                details={"url_id": url_id}
            )
        logger.info(f"URL deleted successfully: {url_id} for user: {current_user.email}")
        return {"message": "URL deleted successfully"}
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error deleting URL: {str(e)} for user: {current_user.email}")
        raise DatabaseError(
            "URL削除中にエラーが発生しました",
            details={"original_error": str(e)} if settings.debug else None
        )


@router.get("/{url_id}/clicks", response_model=List[schemas.ClickResponse])
async def get_url_clicks(
    url_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """URL別クリック履歴取得（認証必須）"""
    logger.info(f"Fetching clicks for URL: {url_id} for user: {current_user.email}")
    
    try:
        clicks = crud.get_clicks_by_url(db, url_id=url_id)
        # クリック時刻もJSTに変換
        click_responses = []
        for click in clicks:
            click_response = schemas.ClickResponse.model_validate(click)
            click_response.clicked_at = convert_to_jst(click.clicked_at)
            click_responses.append(click_response)
        
        logger.info(f"Retrieved {len(click_responses)} clicks for URL: {url_id} for user: {current_user.email}")
        return click_responses
    except Exception as e:
        logger.error(f"Error fetching clicks: {str(e)} for user: {current_user.email}")
        raise DatabaseError(
            "クリック履歴取得中にエラーが発生しました",
            details={"original_error": str(e)} if settings.debug else None
        ) 