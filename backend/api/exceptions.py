"""
Unified exception handling for URL shortener service.
"""
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Dict, Optional
import logging
import traceback
from datetime import datetime

from config import settings

logger = logging.getLogger(__name__)


class BaseAPIException(Exception):
    """基底API例外クラス"""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(BaseAPIException):
    """認証エラー"""
    
    def __init__(self, message: str = "認証に失敗しました", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTHENTICATION_ERROR",
            details=details
        )


class AuthorizationError(BaseAPIException):
    """認可エラー"""
    
    def __init__(self, message: str = "アクセス権限がありません", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AUTHORIZATION_ERROR",
            details=details
        )


class ValidationError(BaseAPIException):
    """バリデーションエラー"""
    
    def __init__(self, message: str = "入力データが無効です", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="VALIDATION_ERROR",
            details=details
        )


class NotFoundError(BaseAPIException):
    """リソース未発見エラー"""
    
    def __init__(self, message: str = "リソースが見つかりません", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND_ERROR",
            details=details
        )


class ConflictError(BaseAPIException):
    """競合エラー"""
    
    def __init__(self, message: str = "リソースが競合しています", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT_ERROR",
            details=details
        )


class DatabaseError(BaseAPIException):
    """データベースエラー"""
    
    def __init__(self, message: str = "データベースエラーが発生しました", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="DATABASE_ERROR",
            details=details
        )


def create_error_response(
    error: BaseAPIException,
    request: Request,
    include_traceback: bool = False
) -> Dict[str, Any]:
    """統一エラーレスポンス作成"""
    
    error_id = f"err_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}"
    
    response_data = {
        "error": {
            "id": error_id,
            "code": error.error_code,
            "message": error.message,
            "status_code": error.status_code,
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url.path),
            "method": request.method
        }
    }
    
    # 詳細情報の追加（開発環境のみ）
    if settings.debug and error.details:
        response_data["error"]["details"] = error.details
    
    # トレースバック情報の追加（開発環境のみ）
    if settings.debug and include_traceback:
        response_data["error"]["traceback"] = traceback.format_exc()
    
    return response_data


async def base_api_exception_handler(request: Request, exc: BaseAPIException) -> JSONResponse:
    """統一API例外ハンドラー"""
    
    # ログ出力
    log_data = {
        "error_code": exc.error_code,
        "message": exc.message,
        "status_code": exc.status_code,
        "path": request.url.path,
        "method": request.method,
        "details": exc.details
    }
    
    if exc.status_code >= 500:
        logger.error(f"Server Error: {log_data}", exc_info=True)
    elif exc.status_code >= 400:
        logger.warning(f"Client Error: {log_data}")
    
    # レスポンス作成
    response_data = create_error_response(exc, request, include_traceback=exc.status_code >= 500)
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTPException用ハンドラー（既存コードとの互換性）"""
    
    # HTTPExceptionをBaseAPIExceptionに変換
    api_exc = BaseAPIException(
        message=str(exc.detail),
        status_code=exc.status_code,
        error_code="HTTP_EXCEPTION"
    )
    
    return await base_api_exception_handler(request, api_exc)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """バリデーションエラー用ハンドラー"""
    
    # バリデーションエラーの詳細を整理
    validation_details = []
    for error in exc.errors():
        validation_details.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    api_exc = ValidationError(
        message="入力データの検証に失敗しました",
        details={"validation_errors": validation_details}
    )
    
    return await base_api_exception_handler(request, api_exc)


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """SQLAlchemyエラー用ハンドラー"""
    
    api_exc = DatabaseError(
        message="データベース操作でエラーが発生しました",
        details={"original_error": str(exc)} if settings.debug else None
    )
    
    return await base_api_exception_handler(request, api_exc)


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """一般例外用ハンドラー"""
    
    api_exc = BaseAPIException(
        message="予期しないエラーが発生しました",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="INTERNAL_SERVER_ERROR",
        details={"original_error": str(exc)} if settings.debug else None
    )
    
    return await base_api_exception_handler(request, api_exc) 