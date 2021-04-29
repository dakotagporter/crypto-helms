"""Executes all core tasks required to function the application."""
# Std Library Imports
from typing import Callable

# Third-party Imports
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