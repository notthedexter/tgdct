from pydantic import BaseModel, Field
from typing import Optional


class ChapterSelectionRequest(BaseModel):
    """Request to select and use a specific chapter"""
    chapter_number: int = Field(..., ge=1, description="Chapter number to use")
    target_language: str = Field(..., description="Target language for the lesson")



class ChapterListResponse(BaseModel):
    """Response listing available chapters"""
    available_chapters: list[int]
    total_chapters: int
    description: Optional[str] = None
