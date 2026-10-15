"""Application: repository interfaces (Dependency Inversion)."""
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.question import Question
from domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    def exists_username(self, username: str) -> bool:
        ...

    @abstractmethod
    def create(self, user: User) -> None:
        ...

    @abstractmethod
    def update_password(self, username: str, new_password: str) -> None:
        ...


class IQuestionRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Question]:
        ...

    @abstractmethod
    def create(self, question: Question) -> int:
        ...

    @abstractmethod
    def update(self, question_id: int, question: Question) -> bool:
        ...

    @abstractmethod
    def delete(self, question_id: int) -> bool:
        ...

    @abstractmethod
    def get_by_ids(self, ids: List[int]) -> List[Question]:
        ...
