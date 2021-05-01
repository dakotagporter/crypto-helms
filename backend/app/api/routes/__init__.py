from fastapi import APIRouter

# Import routes
from app.api.routes.dummy import router as dummy_router
from app.api.routes.forecast import router as forecast_router
from app.api.routes.viz import router as viz_router

# Access all routes with this router
router = APIRouter()

# Include all routes
router.include_router(dummy_router, prefix="/dummy", tags=["dummy"])
router.include_router(forecast_router, prefix="/forecast", tags=["forecast"])