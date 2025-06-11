"""
URL redirect API routes for URL shortener service.
"""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import logging

import crud
import schemas
from database import get_db
from .exceptions import NotFoundError, DatabaseError

logger = logging.getLogger(__name__)

# Create redirect router (no prefix as it handles root-level short codes)
router = APIRouter(tags=["redirect"])


@router.get("/{short_code}")
async def redirect_to_original(short_code: str, request: Request, db: Session = Depends(get_db)):
    """短縮URLから元URLへリダイレクト"""
    logger.info(f"Redirecting: {short_code} from IP: {request.client.host if request.client else 'unknown'}")
    
    try:
        db_url = crud.get_url_by_short_code(db, short_code=short_code)
        if db_url is None:
            logger.warning(f"URL not found for redirect: {short_code}")
            raise NotFoundError(
                "指定された短縮URLが見つかりません",
                details={"short_code": short_code}
            )
        
        # Track click
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "")
        referer = request.headers.get("referer", "")
        
        click_data = schemas.ClickCreate(
            user_agent=user_agent,
            ip_address=client_ip,
            referrer=referer
        )
        
        # クリック記録とカウント更新
        crud.create_click(db=db, url_id=db_url.id, click=click_data)
        crud.increment_click_count(db=db, url_id=db_url.id)
        
        logger.info(f"Click tracked for {short_code}, redirecting to {db_url.original_url}")
        return RedirectResponse(url=db_url.original_url)
        
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error in redirect for {short_code}: {str(e)}")
        raise DatabaseError(
            "リダイレクト処理中にエラーが発生しました",
            details={"short_code": short_code, "original_error": str(e)}
        ) 