from fastapi import APIRouter

# Import routes
from app.api.routes.forecast import router as forecast_router

# Access all routes with this router
router = APIRouter()

# Include all routes
router.include_router(forecast_router, prefix="/forecast", tags=["forecast"])