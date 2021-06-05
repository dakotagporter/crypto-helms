"""
Aggregation of all application routes into a single router. All created routers are imported here and
added to a single router for access from the app.api.server file.

router:
    - Initial instantiation of a router
    - All routers are aggregated to this router
    - All routers are given a name (to appear in the URL) and a tag (for documentation)
"""
from fastapi import APIRouter

# Import routes
from app.api.routes.dummy import router as dummy_router
from app.api.routes.forecast import router as forecast_router
from app.api.routes.viz import router as viz_router
from app.api.routes.users import router as users_router

# Access all routes with this router
router = APIRouter()

# Include all routes
router.include_router(dummy_router, prefix="/dummy", tags=["dummy"])
router.include_router(forecast_router, prefix="/forecast", tags=["forecast"])
router.include_router(users_router, prefix="/users", tags=["users"])