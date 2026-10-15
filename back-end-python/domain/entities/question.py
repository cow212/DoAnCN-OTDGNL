"""Domain: entity Question (Python convention snake_case)."""
from dataclasses import dataclass


@dataclass
class Question:
    id: int = 0
    content: str = ""
    option_a: str = ""
    option_b: str = ""
    option_c: str = ""
    option_d: str = ""
    correct_answer: str = ""
    subject_category: str = ""
    explanation: str = ""
    exam_code: str = ""
