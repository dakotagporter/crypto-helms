# Std Library/Local Imports
from app.api.routes import router as api_router

# Third-party Imports
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Create application
def get_application():
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

    # Include routers
    app.include_router(api_router, prefix="/api")

    return app

app = get_application()