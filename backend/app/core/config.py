"""
Configures all environment variables from the .env file. Using starlette, this process
is decentralized (to prevent a chain of errors if missing an .env file) and easily
and securely accesses all necessary variables from the .env file. This file is
referenced all across the application.

*Default values can be given for certain variables and each variable must specify a type cast.
"""
# Std Library Imports

# Third Party Imports
from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

# Config allows you to specify a file in which to search for environment variables
config = Config(".env")


# Project Description
PROJECT_NAME="CryptoHelms"
VERSION="v1.0.0-alpha"
API_PREFIX="/api"

# Auth
SECRET_KEY = config("SECRET_KEY", cast=Secret)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, defualt="HS256")
JWT_AUDIENCE = config("JWT_AUDIENCE", cast=str, default="cryptohelms:auth")
JWT_TOKEN_PREFIX = config("JWT_TOKEN_PREFIX", cast=str, default="Bearer")
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    cast=int,
    default=7 * 24 * 60 # one week
)

# Database
RDS_USER = config("RDS_USER", cast=str)
RDS_PASSWORD = config("RDS_PASSWORD", cast=Secret)
RDS_NETLOC = config("RDS_NETLOC", cast=str)
RDS_PORT = config("RDS_PORT", cast=str, default="5432")
RDS_DB_NAME = config("RDS_DB_NAME", cast=str)
RDS_REGION = config("RDS_REGION", cast=str)

DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgres://{RDS_USER}:{RDS_PASSWORD}@{RDS_NETLOC}:{RDS_PORT}"
)

# AWS
AWS_ACCESS_KEY = config("AWS_ACCESS_KEY", cast=str)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", cast=str)