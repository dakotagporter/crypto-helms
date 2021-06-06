"""
Using JWTs (JSON Web Tokens), we can give each user a token that
contains information in an x.y.z (header.payload.signature) format
(x=encoded algorithm, y=encoded username or email, z=base64 encoding
of x and y with an extra secret signature) that will keep a user
logged in for a defined period of time.

JWTMeta:
    - Contains attributes needed for the payload
JWTCreds:
    - Contains attributes used to identify the user
      (email and username in our case)

JWTMeta and JWTCreds are combined and encoded to
create the payload.

AccessToken:
    - Creates the access token and allows for
      customization of token types

"""
# Std Library Imports
from datetime import datetime, timedelta

# Third Party Imports
from pydantic import EmailStr

from app.core.config import JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.core import CoreModel


class JWTMeta(CoreModel):
    # Issuer
    iss: str = "cryptohelms.io"
    # Intended Audience
    aud: str = JWT_AUDIENCE
    # Issued At
    iat: float = datetime.timestamp(datetime.utcnow())
    # Token Expiration
    exp: float = datetime.timestamp(datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


class JWTCreds(CoreModel):
    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    pass


class AccessToken(CoreModel):
    access_token: str
    token_type: str