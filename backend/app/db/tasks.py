# Std Library Imports
import logging

# Third-party Imports
import boto3
import psycopg2
from fastapi import FastAPI
from databases import Database

from app.core import config

logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    # Allow connection quantity between 2 and 10 for now
    #database = Database(DATABASE_URL, min_size=2, max_size=10)
    session = boto3.Session(aws_access_key_id=config.AWS_ACCESS_KEY, aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)
    client = session.client("rds")

    token = client.generate_db_auth_token(DBHostname=config.DATABASE_URL, Port=config.POSTGRES_PORT, DBUsername=config.POSTGRES_USER, Region=config.DATABASE_REGION)

    try:
        conn = psycopg2.connect(host=config.DATABASE_URL, port=config.POSTGRES_PORT, database=POSTGRES_DB, user=POSTGRES_USER, password=token)
        cur = conn.cursor()
        cur.execute("SELECT now()")
        print(cur.fetchall())
        #await database.connect()
        #app.state._db = database
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")

async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")