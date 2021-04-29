"""Collection of database tasks to be executed throughout application runtime."""
# Std Library Imports
import logging

# Third-party Imports
from fastapi import FastAPI
from databases import Database

from app.core import config

logger = logging.getLogger(__name__)

# Connect to database using credentials from core.config
async def connect_to_db(app: FastAPI) -> None:
    # Allow connection quantity between 2 and 10 for now
    database = Database(config.DATABASE_URL, min_size=2, max_size=10)

    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")

# Close database connection
async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")