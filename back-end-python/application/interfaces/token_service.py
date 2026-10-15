"""Application: token service abstraction."""
from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.user import User


class ITokenService(ABC):
    @abstractmethod
    def create_access_token(self, user: User) -> str:
        ...

    @abstractmethod
    def decode_access_token(self, token: str) -> Optional[dict]:
        ...
