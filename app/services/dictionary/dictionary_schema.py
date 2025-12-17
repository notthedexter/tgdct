"""Pydantic models for dictionary service."""
from pydantic import BaseModel
from typing import List


class ImageDetectionResponse(BaseModel):
    """Response model for image object detection."""
    word_in_language: str  # One word in the target language
    

class TextSearchResponse(BaseModel):
    """Response model for text dictionary search."""
    word: str
    syllables: str  # Word broken into syllables
    meanings: List[str]  # Meanings/synonyms in English
    english_sentence: str
    sentence_in_language: str  # Example sentence in the target language
    language: str  # The language code
