"""Application DTO cho exam submission."""
from typing import Annotated, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from application.dto.common import aliases


class QuestionAnswerDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    QuestionId: Annotated[int, Field(validation_alias=aliases("QuestionId"))]
    SelectedAnswer: Annotated[Optional[str], Field(validation_alias=aliases("SelectedAnswer"))] = None


class ExamSubmissionDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Answers: Annotated[Optional[List[QuestionAnswerDto]], Field(validation_alias=aliases("Answers"))] = None
