"""Schemas for listening practice service."""
from pydantic import BaseModel
from typing import List


class ListeningOption(BaseModel):
    """Represents a listening practice option."""
    text: str


class ListeningQuestion(BaseModel):
    """Represents a listening practice question with 4 options."""
    question: str
    options: List[ListeningOption]
    correct_option_index: int


class ListeningResponse(BaseModel):
    """Response containing the generated listening practice."""
    topic: str
    questions: List[ListeningQuestion]


class ListeningRequest(BaseModel):
    """Request to generate listening practice."""
    topic: str
    language: str = "tl-PH"


class ListeningAnswerEvaluation(BaseModel):
    """Evaluation of a submitted answer."""
    is_correct: bool
    correct_answer: str
    explanation: str
