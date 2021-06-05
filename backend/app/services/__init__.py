"""
Create a single instatiation of our AuthService to be used throughout the application.
"""
from app.services.authentication import AuthService

auth_service = AuthService()