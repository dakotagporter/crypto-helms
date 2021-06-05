"""
Source file called upon by docker-compose on application initialization. This file
instantiates a FastAPI application and wraps the commands in a function so a single
variable can hold the instance to be referenced by other resources throughout the app.

get_application():
    - Factory function that instantiates a FastAPI app with given metadata
    - Adds middleware for app to communicate with other resources like HTTP
      and databases, etc. (more than what's provided from an OS)
    - Event handlers perform operations at startup and shutdown of the app
    - Includes a single router (one that has already aggregated the rest of the routers)
      to give the app access to all API endpoints
"""
# Std Library Imports

# Third Party Imports
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

    # Include event handlers (functions executed on starting and closing of application)
    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    # All api routes sent to app
    app.include_router(api_router, prefix="/api")

    return app

app = get_application()