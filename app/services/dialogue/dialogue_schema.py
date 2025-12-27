"""Schemas for dialogue builder service."""
from pydantic import BaseModel
from typing import List


class DialogueOption(BaseModel):
    """Represents a dialogue option."""
    text: str  # Option in target language
    english_text: str  # Option in English


class DialogueQuestion(BaseModel):
    """Represents a dialogue question with options."""
    question: str  # Question in target language
    question_english: str  # Question in English
    options: List[DialogueOption]
    correct_option_index: int


class DialogueResponse(BaseModel):
    """Response containing the generated dialogue."""
    scenario: str
    questions: List[DialogueQuestion]


class DialogueRequest(BaseModel):
    """Request to generate a dialogue."""
    scenario: str
    language: str = "en-US"


class AnswerEvaluation(BaseModel):
    """Evaluation of a submitted answer."""
    is_correct: bool
    correct_answer: str
    explanation: str
