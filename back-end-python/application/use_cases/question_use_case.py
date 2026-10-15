"""Application use case cho question."""
from typing import List

from application.dto.question import QuestionDto
from application.interfaces.repositories import IQuestionRepository
from domain.entities.question import Question


def _to_domain(dto: QuestionDto) -> Question:
    return Question(
        id=dto.Id,
        content=dto.Content,
        option_a=dto.OptionA,
        option_b=dto.OptionB,
        option_c=dto.OptionC,
        option_d=dto.OptionD,
        correct_answer=dto.CorrectAnswer,
        subject_category=dto.SubjectCategory,
        explanation=dto.Explanation,
        exam_code=dto.ExamCode,
    )


def _to_dto(entity: Question) -> QuestionDto:
    return QuestionDto(
        Id=entity.id,
        Content=entity.content,
        OptionA=entity.option_a,
        OptionB=entity.option_b,
        OptionC=entity.option_c,
        OptionD=entity.option_d,
        CorrectAnswer=entity.correct_answer,
        SubjectCategory=entity.subject_category,
        Explanation=entity.explanation,
        ExamCode=entity.exam_code,
    )


class QuestionUseCase:
    def __init__(self, question_repo: IQuestionRepository):
        self._question_repo = question_repo

    def get_all(self) -> List[QuestionDto]:
        return [_to_dto(q) for q in self._question_repo.get_all()]

    def create(self, dto: QuestionDto) -> QuestionDto:
        new_id = self._question_repo.create(_to_domain(dto))
        dto.Id = new_id
        return dto

    def update(self, question_id: int, dto: QuestionDto) -> QuestionDto:
        ok = self._question_repo.update(question_id, _to_domain(dto))
        if not ok:
            raise ValueError("Không tìm thấy câu hỏi để cập nhật.")
        dto.Id = question_id
        return dto

    def delete(self, question_id: int) -> None:
        ok = self._question_repo.delete(question_id)
        if not ok:
            raise ValueError("Không tìm thấy câu hỏi để xóa.")
