"""Infrastructure: JWT implementation (PyJWT)."""
import os
from datetime import datetime, timedelta, timezone

import jwt

from application.interfaces.token_service import ITokenService
from domain.entities.user import User

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-this-in-production-32chars+")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24


class JwtTokenService(ITokenService):
    def create_access_token(self, user: User) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
        payload = {
            "sub": user.username,
            "role": user.role,
            "user_id": user.id,
            "exp": expire,
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    def decode_access_token(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except jwt.PyJWTError:
            return None
