# Std Library/Local Imports
from app.api import forecast

# Third-party Imports
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Instantiate app and app metadata
app = FastAPI(
    title = "CryptoHelms",
    description = "Production web application for cryptocurrency time-series predictions.",
    version = "0.1"
)

# Include middleware to handle requests from other origins (IP addresses, ports, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    forecast.router,
    tags=["Forecast"],
)

if __name__ == '__main__':
    uvicorn.run(app)