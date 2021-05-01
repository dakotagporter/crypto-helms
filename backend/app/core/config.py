from starlette.config import Config
from starlette.datastructures import Secret

# Config allows to specify a file in which to search for environment variables
config = Config(".env")

# Project Description
PROJECT_NAME="CryptoHelms"
VERSION="v1.0.0-alpha"
API_PREFIX="/api"

# Secret Key
SECRET_KEY = config("SECRET_KEY", cast=Secret, default="NEWKEY")

# Database
RDS_USER = config("RDS_USER", cast=str)
RDS_PASSWORD = config("RDS_PASSWORD", cast=Secret)
RDS_PORT = config("RDS_PORT", cast=str, default="5432")
RDS_DB_NAME = config("RDS_DB_NAME", cast=str)
RDS_REGION = config("RDS_REGION", cast=str)
DATABASE_URL = config("DATABASE_URL", cast=str)
RFC1738_DATABASE_URL = config("RFC1738_DATABASE_URL", cast=str)

# AWS
AWS_ACCESS_KEY = config("AWS_ACCESS_KEY", cast=str)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", cast=str)