from fastapi import APIRouter

# Instantiate router
router = APIRouter()

# Create visualizations endpoint
@router.get("/viz")
async def viz():
    # Endpoint used for any visualizations
    return {"Endpoint:": "/viz"}