"""Application DTO cho auth."""
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field

from application.dto.common import aliases


class LoginDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Username: Annotated[Optional[str], Field(validation_alias=aliases("Username"))] = None
    Password: Annotated[Optional[str], Field(validation_alias=aliases("Password"))] = None


class RegisterDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Username: Annotated[Optional[str], Field(validation_alias=aliases("Username"))] = None
    Password: Annotated[Optional[str], Field(validation_alias=aliases("Password"))] = None
    FullName: Annotated[Optional[str], Field(validation_alias=aliases("FullName"))] = None


class ChangePasswordDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Username: Annotated[Optional[str], Field(validation_alias=aliases("Username"))] = None
    OldPassword: Annotated[Optional[str], Field(validation_alias=aliases("OldPassword"))] = None
    NewPassword: Annotated[Optional[str], Field(validation_alias=aliases("NewPassword"))] = None
