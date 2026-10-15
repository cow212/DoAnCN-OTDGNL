"""Presentation: Exam router."""
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from application.dto.exam import ExamSubmissionDto
from application.use_cases.exam_use_case import ExamUseCase
from infrastructure.repositories.sql_question_repository import SqlQuestionRepository


router = APIRouter(prefix="/exam", tags=["Exam"])


@router.post("/submit")
async def submit_exam(submission: Optional[ExamSubmissionDto] = None):
    if submission is None or not submission.Answers:
        return PlainTextResponse(content="Bài làm không có dữ liệu trả lời.", status_code=400)

    use_case = ExamUseCase(SqlQuestionRepository())
    result = use_case.submit(submission)
    return {
        "TotalQuestions": result.total_questions,
        "CorrectCount": result.correct_count,
        "ScorePercentage": result.score_percentage,
        "Details": result.details,
    }
