from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

# Config allows to specify a file in which to search for environment variables
config = Config(".env")

PROJECT_NAME="CryptoHelms"
VERSION="v1.0.0-alpha"
API_PREFIX="/api"

SECRET_KEY = config("SECRET_KEY", cast=Secret, default="NEWKEY")

# Database
POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)
DATABASE_URL = config("DATABASE_URL", cast=str)
DATABASE_REGION = config("DATABASE_REGION", cast=str)

# AWS
AWS_ACCESS_KEY = config("AWS_ACCESS_KEY", cast=str)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", cast=str)