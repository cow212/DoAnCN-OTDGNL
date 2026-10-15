"""Infrastructure: SQL Server implementation of IUserRepository."""
import pyodbc

from application.interfaces.repositories import IUserRepository
from domain.entities.user import User
from infrastructure.db.connection import get_db


class SqlUserRepository(IUserRepository):
    def exists_username(self, username: str) -> bool:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM Users WHERE Username = ?", username)
            return (cur.fetchone()[0] or 0) > 0

    def create(self, user: User) -> None:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Users (Username, Password, Role, FullName) VALUES (?, ?, ?, ?)",
                user.username,
                user.password,
                user.role,
                user.full_name,
            )

    def get_by_credentials(self, username: str, password: str) -> User | None:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT Id, Username, Password, Role, FullName FROM Users "
                "WHERE Username = ? AND Password = ?",
                username,
                password,
            )
            row = cur.fetchone()
        if row is None:
            return None
        return User(
            id=int(row[0]),
            username=row[1] or "",
            password=row[2] or "",
            role=row[3] or "",
            full_name=row[4] or "",
        )

    def update_password(self, username: str, new_password: str) -> None:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE Users SET Password = ? WHERE Username = ?",
                new_password,
                username,
            )
