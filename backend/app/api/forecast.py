from fastapi import APIRouter

# Instantiate router
router = APIRouter()

@router.get("/forecast")
async def forecast():
    # Retrieve user's input.
    # Send input to SageMaker endpoint.
    # Return estimator prediction.
    return {"Endpoint:": "/forecast"}
