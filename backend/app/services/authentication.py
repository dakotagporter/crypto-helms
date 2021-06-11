"""
Deal with user authentication.

create_salt_and_hashed_password():
    - Takes a plaintext string (password the user entered) and uses the
      generate_salt() and hash_password() functions to hash the password
    - Returns a user model containing the hashed password and the salt used

generate_salt():
    - Generates salt for the users password

hash_password():
    - Creates a hash of the combination of the users generated hash and plaintext password

verify_password():
    - Use CryptContexts verify function to verify that a users password is hashed

create_access_token_for_user():
    - Takes a user from the db and creates the meta and creds for
      the user with out JWTMeta and JWTCreds classes
    - All of those attributes are dumped into a JWTPayload object
    - The payload is the encoded with our algorithm and secret key

get_username_from_token():
    - Attempts to decode a token and raises an error if there is an issue
    - Returns the username if successful
"""
# Std Library Imports
from datetime import datetime, timedelta
from typing import Optional

# Third Party Imports
import jwt
import bcrypt
from pydantic import ValidationError
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.models.user import UserPasswordUpdate
from app.core.config import SECRET_KEY, JWT_AUDIENCE, JWT_ALGORITHM, JWT_TOKEN_PREFIX, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.token import JWTMeta, JWTCreds, JWTPayload
from app.models.user import UserPasswordUpdate, UserInDB


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(BaseException):
    """
    Custom auth exceptions.
    """
    pass


class AuthService:
    def create_salt_and_hashed_password(self, *, plaintext_password: str) -> UserPasswordUpdate:
        salt = self.generate_salt()
        hashed_password = self.hash_password(password=plaintext_password, salt=salt)

        return UserPasswordUpdate(salt=salt, password=hashed_password)
    
    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode()
    
    def hash_password(self, *, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)
    
    def verify_password(self, *, password: str, salt: str, hashed_pw: str) -> bool:
        return pwd_context.verify(password + salt, hashed_pw)
    
    def create_access_token_for_user(
        self,
        *,
        user: UserInDB,
        secret_key: str = str(SECRET_KEY),
        audience: str = str(JWT_AUDIENCE),
        expires_in: int = int(ACCESS_TOKEN_EXPIRE_MINUTES)
    ) -> str:
        if not user or not isinstance(user, UserInDB):
            return None
        
        jwt_meta = JWTMeta(
            aud=audience,
            iat=datetime.timestamp(datetime.utcnow()),
            exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in))
        )
        jwt_creds = JWTCreds(sub=user.email, username=user.username)
        token_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_creds.dict()
        )

        access_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)

        return access_token
    
    def get_username_from_token(self, *, token: str, secret_key: str) -> Optional[str]:
        try:
            decoded_token = jwt.decode(token, str(secret_key), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
            payload = JWTPayload(**decoded_token)
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token credentials.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return payload.username