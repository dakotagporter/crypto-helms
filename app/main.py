# Std Library/Local Imports
from api import prediction

# Third-party Imports
import uvicorn
from fastapi import FastAPI


# Instantiate app and app metadata
app = FastAPI(
    title = "CryptoHelms",
    description = "Production web application for cryptocurrency time-series predictions.",
    version = "0.1"
)

# Endpoints
@app.get("/")
async def root():
    """
    Example route containing a simple JSON return object.
    """
    return {"message": "Hello, World!"}

app.include_router(
    prediction.router,
    tags=["Submission"],
)

if __name__ == '__main__':
    uvicorn.run(app)