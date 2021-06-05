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
"""
# Std Library Imports

# Third Party Imports
import bcrypt
from passlib.context import CryptContext

from app.models.user import UserPasswordUpdate


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