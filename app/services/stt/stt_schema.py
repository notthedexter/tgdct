"""Pydantic schemas for STT (Speech-to-Text) service."""
from pydantic import BaseModel, Field
from typing import Optional


class SpeechToTextResponse(BaseModel):
    """Response schema for speech-to-text transcription."""
    
    text: str = Field(..., description="Transcribed text from audio")
    language: str = Field(..., description="Language used for transcription")
    detected_language: Optional[str] = Field(None, description="Detected language from audio if different")
