"""Application DTO cho Question (request/response dùng chung)."""
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from application.dto.common import aliases


class QuestionDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Id: Annotated[int, Field(validation_alias=aliases("Id"))] = 0
    Content: Annotated[str, Field(validation_alias=aliases("Content"))] = ""
    OptionA: Annotated[str, Field(validation_alias=aliases("OptionA"))] = ""
    OptionB: Annotated[str, Field(validation_alias=aliases("OptionB"))] = ""
    OptionC: Annotated[str, Field(validation_alias=aliases("OptionC"))] = ""
    OptionD: Annotated[str, Field(validation_alias=aliases("OptionD"))] = ""
    CorrectAnswer: Annotated[str, Field(validation_alias=aliases("CorrectAnswer"))] = ""
    SubjectCategory: Annotated[str, Field(validation_alias=aliases("SubjectCategory"))] = ""
    Explanation: Annotated[str, Field(validation_alias=aliases("Explanation"))] = ""
    ExamCode: Annotated[str, Field(validation_alias=aliases("ExamCode"))] = ""
