"""Collection of database tasks to be executed throughout application runtime."""
# Std Library Imports
import logging

# Third-party Imports
from fastapi import FastAPI
import psycopg2
import boto3

from app.core import config

logger = logging.getLogger(__name__)

# Connect to database using credentials from core.config
async def connect_to_db(app: FastAPI) -> None:

    try:
        # Connect to database
        conn = psycopg2.connect(
            host=config.DATABASE_URL,
            port=config.RDS_PORT,
            database=config.RDS_DB_NAME,
            user=config.RDS_USER,
            password=config.RDS_PASSWORD
            )
        
        # Establish app database connection state
        app.state._db = conn

    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")

# Close database connection
async def close_db_connection(app: FastAPI) -> None:
    try:
        app.state._db.close()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")