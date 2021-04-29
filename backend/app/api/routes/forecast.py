from fastapi import APIRouter

# Instantiate router
router = APIRouter()

# Forecast router to generate predictions and return to user.
@router.get("/")
async def forecast():
    # Retrieve user's input.
    # Send input to SageMaker endpoint.
    # Return estimator prediction.
    return {"Endpoint:": "/forecast"}
