"""Application use case cho auth."""
import re
from dataclasses import dataclass
from typing import Optional

from application.dto.auth import ChangePasswordDto, LoginDto, RegisterDto
from application.interfaces.repositories import IUserRepository
from application.interfaces.token_service import ITokenService
from domain.entities.user import User


_SPECIAL_CHAR_RE = re.compile(r"[!@#$%^&*(),.?:{}|<>\-_+=~`\[\]\\/]")


@dataclass
class RegisterResult:
    status_code: int
    message: str


@dataclass
class LoginResult:
    status_code: int
    message: str
    payload: Optional[dict] = None


class AuthUseCase:
    def __init__(self, user_repo: IUserRepository, token_service: Optional[ITokenService] = None):
        self._user_repo = user_repo
        # Token service có thể None khi test, nhưng production luôn truyền vào.
        self._token_service = token_service
        self._user_repo = user_repo

    def register(self, dto: RegisterDto) -> RegisterResult:
        if not dto.Username or not dto.Password:
            return RegisterResult(400, "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")

        has_number = bool(re.search(r"[0-9]", dto.Password))
        has_special = bool(_SPECIAL_CHAR_RE.search(dto.Password))
        if not has_number or not has_special:
            return RegisterResult(
                400,
                "Mật khẩu bảo mật yếu: Phải chứa ít nhất một chữ số và một ký tự đặc biệt!",
            )

        if self._user_repo.exists_username(dto.Username):
            return RegisterResult(400, "Tên đăng nhập này đã có người đăng ký. Vui lòng chọn tên khác!")

        user = User(
            username=dto.Username,
            password=dto.Password,
            role="Student",
            full_name=dto.FullName or "",
        )
        self._user_repo.create(user)
        return RegisterResult(200, "Đăng ký tài khoản thành công! Bạn có thể đăng nhập ngay bây giờ.")

    def login(self, dto: LoginDto) -> LoginResult:
        if not dto.Username or not dto.Password:
            return LoginResult(400, "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")

        user = self._user_repo.get_by_credentials(dto.Username, dto.Password)
        if user is None:
            return LoginResult(401, "Tài khoản hoặc mật khẩu không chính xác.")

        # Tạo JWT token để client dùng cho các API cần quyền (ví dụ admin thêm đề).
        access_token = None
        if self._token_service is not None:
            access_token = self._token_service.create_access_token(user)

        payload = {
            "Message": "Đăng nhập thành công!",
            "UserId": user.id,
            "Username": user.username,
            "FullName": user.full_name,
            "Role": user.role,
            "AccessToken": access_token,
        }
        return LoginResult(200, "Đăng nhập thành công!", payload)

    def change_password(self, dto: ChangePasswordDto) -> RegisterResult:
        if not dto.Username or not dto.OldPassword or not dto.NewPassword:
            return RegisterResult(400, "Vui lòng nhập đầy đủ thông tin đổi mật khẩu.")

        user = self._user_repo.get_by_credentials(dto.Username, dto.OldPassword)
        if user is None:
            return RegisterResult(401, "Tài khoản hoặc mật khẩu cũ không chính xác.")

        has_number = bool(re.search(r"[0-9]", dto.NewPassword))
        has_special = bool(_SPECIAL_CHAR_RE.search(dto.NewPassword))
        if not has_number or not has_special:
            return RegisterResult(
                400,
                "Mật khẩu mới bảo mật yếu: Phải chứa ít nhất một chữ số và một ký tự đặc biệt!",
            )

        self._user_repo.update_password(dto.Username, dto.NewPassword)
        return RegisterResult(200, "Đổi mật khẩu thành công!")
