from datetime import datetime, timedelta, timezone
from typing import NamedTuple
from uuid import UUID

import jwt
from pydantic import BaseModel, ValidationError

from app.core.config import settings


class IssuedToken(NamedTuple):
    token: str

class TokenPayload(BaseModel):
    sub: UUID
    username: str
    exp: int
    iat: int

class TokenError(Exception): ...


class InvalidTokenError(TokenError): ...


class ExpiredTokenError(TokenError): ...


def create_access_token(user_id: UUID, username: str) -> IssuedToken:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    claims = {
        "sub": str(user_id),
        "username": username,
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp()),
    }

    token = jwt.encode(
        claims,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return IssuedToken(token=token)

def decode_access_token(token: str) -> TokenPayload:
    try:
        raw = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()

    try:
        return TokenPayload(**raw)
    except ValidationError:
        raise InvalidTokenError()