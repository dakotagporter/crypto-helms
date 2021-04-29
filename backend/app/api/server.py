# Std Library Imports


# Third-party Imports
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import config, tasks
from app.api.routes import router as api_router


# Create application
def get_application():
    # Instantiate app and app metadata
    app = FastAPI(
        title = config.PROJECT_NAME,
        description = "Production web application for cryptocurrency time-series predictions.",
        version = config.VERSION
    )

    # Include middleware to handle requests from other origins (IP addresses, ports, etc.)
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Include event handlers
    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    # Include routers
    app.include_router(api_router, prefix="/api")

    return app

app = get_application()