"""Collection of database tasks to be executed throughout application runtime."""
# Std Library Imports
import logging

# Third-party Imports
from databases import Database
from fastapi import FastAPI
import boto3

from app.core import config

logger = logging.getLogger(__name__)

# Connect to database using credentials from core.config
async def connect_to_db(app: FastAPI) -> None:

    try:
        # Connect to database
        database = Database(config.DATABASE_URL)

        # Establish app database connection state
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