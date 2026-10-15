"""Application use case cho chấm bài thi."""
from dataclasses import dataclass
from typing import List

from application.dto.exam import ExamSubmissionDto
from application.dto.question import QuestionDto
from application.interfaces.repositories import IQuestionRepository
from domain.entities.question import Question


@dataclass
class ExamResult:
    total_questions: int
    correct_count: int
    score_percentage: float
    details: List[dict]


class ExamUseCase:
    def __init__(self, question_repo: IQuestionRepository):
        self._question_repo = question_repo

    def submit(self, submission: ExamSubmissionDto) -> ExamResult:
        answers = submission.Answers or []
        if not answers:
            raise ValueError("Bài làm không có dữ liệu trả lời.")

        question_ids = [int(a.QuestionId) for a in answers]
        questions = {q.id: q for q in self._question_repo.get_by_ids(question_ids)}

        correct_count = 0
        details: List[dict] = []
        for answer in answers:
            question = questions.get(int(answer.QuestionId))
            if question is None:
                continue
            is_correct = (
                str(question.correct_answer or "").strip().lower()
                == str(answer.SelectedAnswer or "").strip().lower()
            )
            if is_correct:
                correct_count += 1

            details.append(
                {
                    "questionId": question.id,
                    "content": question.content,
                    "selectedAnswer": answer.SelectedAnswer,
                    "correctAnswer": question.correct_answer,
                    "isCorrect": is_correct,
                    "explanation": question.explanation,
                }
            )

        total = len(answers)
        score = round((correct_count / total) * 100, 2)
        return ExamResult(
            total_questions=total,
            correct_count=correct_count,
            score_percentage=score,
            details=details,
        )
