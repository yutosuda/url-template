"""
API routes for URL shortener service.
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import pytz

import crud
import schemas
from database import get_db
from config import settings
from utils.logging import get_logger
from utils.validators import is_valid_url, is_safe_url

logger = get_logger(__name__)

# Create API router
router = APIRouter()

# 日本のタイムゾーン
JST = pytz.timezone('Asia/Tokyo')

def convert_to_jst(utc_datetime):
    """UTC時刻をJST時刻に変換する"""
    if utc_datetime.tzinfo is None:
        # タイムゾーン情報がない場合はUTCとして扱う
        utc_datetime = pytz.utc.localize(utc_datetime)
    return utc_datetime.astimezone(JST)

@router.post("/api/urls", response_model=schemas.URLResponse)
def create_url(url: schemas.URLCreate, request: Request, db: Session = Depends(get_db)):
    """Create a new shortened URL."""
    logger.info(f"Creating URL: {url.original_url}")
    
    # Validate URL
    if not is_valid_url(str(url.original_url)):
        logger.warning(f"Invalid URL format: {url.original_url}")
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    if not is_safe_url(str(url.original_url)):
        logger.warning(f"Unsafe URL blocked: {url.original_url}")
        raise HTTPException(status_code=400, detail="URL not allowed")
    
    try:
        db_url = crud.create_url(db=db, url_create=url)
        
        # レスポンス用に短縮URLを生成
        short_url = f"{settings.base_url}/r/{db_url.short_code}"
        
        response = schemas.URLResponse(
            id=db_url.id,
            original_url=db_url.original_url,
            short_code=db_url.short_code,
            click_count=db_url.click_count,
            created_at=convert_to_jst(db_url.created_at),
            short_url=short_url
        )
        
        logger.info(f"URL created successfully: {db_url.short_code}")
        return response
    except Exception as e:
        logger.error(f"Error creating URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/urls", response_model=schemas.URLList)
def read_urls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of URLs."""
    logger.info(f"Fetching URLs: skip={skip}, limit={limit}")
    
    try:
        urls = crud.get_urls(db, skip=skip, limit=limit)
        total = crud.get_urls_count(db)
        
        # レスポンス用にshort_urlを追加
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
        
        return schemas.URLList(urls=url_responses, total=total)
    except Exception as e:
        logger.error(f"Error fetching URLs: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/urls/{short_code}", response_model=schemas.URLResponse)
def read_url(short_code: str, db: Session = Depends(get_db)):
    """Get URL by short code."""
    logger.info(f"Fetching URL: {short_code}")
    
    try:
        db_url = crud.get_url_by_short_code(db, short_code=short_code)
        if db_url is None:
            logger.warning(f"URL not found: {short_code}")
            raise HTTPException(status_code=404, detail="URL not found")
        
        short_url = f"{settings.base_url}/r/{db_url.short_code}"
        return schemas.URLResponse(
            id=db_url.id,
            original_url=db_url.original_url,
            short_code=db_url.short_code,
            click_count=db_url.click_count,
            created_at=convert_to_jst(db_url.created_at),
            short_url=short_url
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/api/urls/{short_code}")
def delete_url(short_code: str, db: Session = Depends(get_db)):
    """Delete a URL by short code."""
    logger.info(f"Deleting URL: {short_code}")
    
    try:
        db_url = crud.get_url_by_short_code(db, short_code=short_code)
        if db_url is None:
            logger.warning(f"URL not found for deletion: {short_code}")
            raise HTTPException(status_code=404, detail="URL not found")
        
        crud.delete_url(db=db, url_id=db_url.id)
        logger.info(f"URL deleted successfully: {short_code}")
        return {"message": "URL deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/r/{short_code}")
def redirect_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    """Redirect to original URL and track click."""
    logger.info(f"Redirecting: {short_code}")
    
    try:
        db_url = crud.get_url_by_short_code(db, short_code=short_code)
        if db_url is None:
            logger.warning(f"URL not found for redirect: {short_code}")
            raise HTTPException(status_code=404, detail="URL not found")
        
        # Track click
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "")
        referer = request.headers.get("referer", "")
        
        click_data = schemas.ClickCreate(
            user_agent=user_agent,
            ip_address=client_ip,
            referrer=referer
        )
        crud.create_click(db=db, url_id=db_url.id, click_data=click_data)
        crud.increment_click_count(db=db, url_id=db_url.id)
        
        logger.info(f"Click tracked for {short_code}, redirecting to {db_url.original_url}")
        return RedirectResponse(url=db_url.original_url)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in redirect: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/urls/{short_code}/clicks", response_model=List[schemas.ClickResponse])
def read_clicks(short_code: str, db: Session = Depends(get_db)):
    """Get click history for a URL."""
    logger.info(f"Fetching clicks for: {short_code}")
    
    try:
        db_url = crud.get_url_by_short_code(db, short_code=short_code)
        if db_url is None:
            logger.warning(f"URL not found: {short_code}")
            raise HTTPException(status_code=404, detail="URL not found")
        
        clicks = crud.get_clicks_by_url(db, url_id=db_url.id)
        # クリック時刻もJSTに変換
        click_responses = []
        for click in clicks:
            click_response = schemas.ClickResponse.from_orm(click)
            click_response.clicked_at = convert_to_jst(click.clicked_at)
            click_responses.append(click_response)
        return click_responses
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching clicks: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/stats", response_model=schemas.URLStats)
def get_stats(db: Session = Depends(get_db)):
    """Get application statistics."""
    logger.info("Fetching application statistics")
    
    try:
        total_urls = crud.get_urls_count(db)
        total_clicks = crud.get_total_clicks(db)
        top_urls_data = crud.get_top_urls(db, limit=5)
        
        # トップURLのレスポンス形式に変換
        top_urls = []
        for url in top_urls_data:
            short_url = f"{settings.base_url}/r/{url.short_code}"
            top_urls.append(schemas.URLResponse(
                id=url.id,
                original_url=url.original_url,
                short_code=url.short_code,
                click_count=url.click_count,
                created_at=convert_to_jst(url.created_at),
                short_url=short_url
            ))
        
        return schemas.URLStats(
            total_urls=total_urls,
            total_clicks=total_clicks,
            top_urls=top_urls
        )
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") 