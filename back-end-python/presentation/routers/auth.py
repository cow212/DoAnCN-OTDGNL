"""Presentation: Auth router."""
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, JSONResponse

from application.dto.auth import ChangePasswordDto, LoginDto, RegisterDto
from application.use_cases.auth_use_case import AuthUseCase
from infrastructure.repositories.sql_user_repository import SqlUserRepository
from infrastructure.security.jwt_token_service import JwtTokenService

router = APIRouter(prefix="/auth", tags=["Auth"])

# Tạo 1 service token dùng chung
_token_service = JwtTokenService()


@router.post("/register")
async def register(model: RegisterDto):
    use_case = AuthUseCase(SqlUserRepository(), _token_service)
    result = use_case.register(model)
    if result.status_code != 200:
        return PlainTextResponse(content=result.message, status_code=result.status_code)
    return JSONResponse(status_code=200, content={"Message": result.message})


@router.post("/login")
async def login(model: LoginDto):
    use_case = AuthUseCase(SqlUserRepository(), _token_service)
    result = use_case.login(model)
    if result.payload is None:
        return PlainTextResponse(content=result.message, status_code=result.status_code)
    return result.payload


@router.post("/change-password")
async def change_password(model: ChangePasswordDto):
    use_case = AuthUseCase(SqlUserRepository(), _token_service)
    result = use_case.change_password(model)
    if result.status_code != 200:
        return PlainTextResponse(content=result.message, status_code=result.status_code)
    return JSONResponse(status_code=200, content={"Message": result.message})
