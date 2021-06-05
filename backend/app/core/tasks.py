"""Executes all core tasks required to function the application.

create_start_app_handler():
    - Used in startup event handler in app.api.server
    - Connects to our database
    - Returns function to be executed on startup

create_stop_app_handler():
    - Used in shutdown event handler in app.api.server
    - Closes the database connection
    - Returns function to be executed on shutdown
"""
# Std Library Imports
from typing import Callable

# Third Party Imports
from fastapi import FastAPI

from app.db.tasks import connect_to_db, close_db_connection

# Returns a function that is called when app is started
def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await connect_to_db(app)
    
    return start_app

# Returns a function that is called when app is terminated
def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app