"""
Main API router that combines all feature-specific routers.
This file serves as the central routing hub for the URL shortener service.
"""
from fastapi import APIRouter

# Import feature-specific routers
from .auth import router as auth_router
from .urls import router as urls_router
from .redirect import router as redirect_router
from .stats import router as stats_router
from .health import router as health_router

# Create main API router
router = APIRouter()

# Include all feature routers (ヘルスチェックを最優先)
# Note: redirect_router は main.py で個別に登録（プレフィックスなし）
router.include_router(health_router)
router.include_router(auth_router)
router.include_router(urls_router)
router.include_router(stats_router) 