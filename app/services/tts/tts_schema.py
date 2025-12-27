"""Pydantic schemas for TTS (Text-to-Speech) service."""
from pydantic import BaseModel, Field


class TextToSpeechRequest(BaseModel):
    """Request schema for text-to-speech conversion."""
    language: str = Field(..., description="Language code (en-US for English, tl-PH for Tagalog)")
    text: str = Field(..., description="Text to convert to speech")