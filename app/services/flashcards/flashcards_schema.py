"""Pydantic models for flashcards service."""
from pydantic import BaseModel
from typing import List


class FlashcardItem(BaseModel):
    """Model for a single flashcard item."""
    syllables: str  # Pronunciation syllables with stress
    meaning: str  # Meaning in English
    topic_name: str  # Topic name in English
    sub_topic_name: str  # Sub-topic name in English
    word: str  # The word in the target language
    english_meaning: str  # English meaning


class FlashcardResponse(BaseModel):
    """Response model for flashcard generation."""
    flashcards: List[FlashcardItem]  # List of 5 flashcard items
    language: str  # The language code