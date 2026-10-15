"""Infrastructure: SQL Server implementation of IQuestionRepository."""
from typing import List

from application.interfaces.repositories import IQuestionRepository
from domain.entities.question import Question
from infrastructure.db.connection import get_db


class SqlQuestionRepository(IQuestionRepository):
    _COLUMNS = [
        "Id", "Content", "OptionA", "OptionB", "OptionC", "OptionD",
        "CorrectAnswer", "SubjectCategory", "Explanation", "ExamCode",
    ]

    def _row_to_question(self, row) -> Question:
        data = dict(zip(self._COLUMNS, row))
        return Question(
            id=int(data["Id"]),
            content=data["Content"] or "",
            option_a=data["OptionA"] or "",
            option_b=data["OptionB"] or "",
            option_c=data["OptionC"] or "",
            option_d=data["OptionD"] or "",
            correct_answer=data["CorrectAnswer"] or "",
            subject_category=data["SubjectCategory"] or "",
            explanation=data["Explanation"] or "",
            exam_code=data.get("ExamCode") or "",
        )

    def get_all(self) -> List[Question]:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT Id, Content, OptionA, OptionB, OptionC, OptionD, "
                "CorrectAnswer, SubjectCategory, Explanation, ExamCode "
                "FROM Questions ORDER BY Id"
            )
            return [self._row_to_question(row) for row in cur.fetchall()]

    def create(self, question: Question) -> int:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Questions "
                "(Content, OptionA, OptionB, OptionC, OptionD, CorrectAnswer, "
                "SubjectCategory, Explanation, ExamCode) "
                "OUTPUT INSERTED.Id "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                question.content,
                question.option_a,
                question.option_b,
                question.option_c,
                question.option_d,
                question.correct_answer,
                question.subject_category,
                question.explanation,
                question.exam_code,
            )
            row = cur.fetchone()
            return int(row[0]) if row and row[0] is not None else 0

    def update(self, question_id: int, question: Question) -> bool:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE Questions SET "
                "Content=?, OptionA=?, OptionB=?, OptionC=?, OptionD=?, "
                "CorrectAnswer=?, SubjectCategory=?, Explanation=?, ExamCode=? "
                "WHERE Id=?",
                question.content,
                question.option_a,
                question.option_b,
                question.option_c,
                question.option_d,
                question.correct_answer,
                question.subject_category,
                question.explanation,
                question.exam_code,
                question_id,
            )
            return cur.rowcount > 0

    def delete(self, question_id: int) -> bool:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM Questions WHERE Id = ?", question_id)
            return cur.rowcount > 0

    def get_by_ids(self, ids: List[int]) -> List[Question]:
        if not ids:
            return []
        placeholders = ", ".join("?" for _ in ids)
        sql = (
            "SELECT Id, Content, OptionA, OptionB, OptionC, OptionD, "
            "CorrectAnswer, SubjectCategory, Explanation, ExamCode "
            f"FROM Questions WHERE Id IN ({placeholders})"
        )
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute(sql, *ids)
            return [self._row_to_question(row) for row in cur.fetchall()]
