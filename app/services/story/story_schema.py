"""Schemas for AI story service."""
from pydantic import BaseModel


class StoryRequest(BaseModel):
    """Request to generate a story."""
    topic: str
    language: str = "tl-PH"


class StoryResponse(BaseModel):
    """Response containing the generated story."""
    topic: str
    story_target_language: str
    story_english: str
    language: str