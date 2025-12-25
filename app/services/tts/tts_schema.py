"""Pydantic schemas for TTS (Text-to-Speech) service."""
from pydantic import BaseModel, Field
from typing import Optional


class TextToSpeechRequest(BaseModel):
    """Request schema for text-to-speech conversion."""

    text: str = Field(..., description="Text to convert to speech")
    language: str = Field(default="tl-PH", description="Language for speech synthesis (BCP-47 code)")


class TextToSpeechResponse(BaseModel):
    """Response schema for text-to-speech conversion."""

    file_location: str = Field(..., description="Location where the audio file is stored")
    voice: str = Field(..., description="Voice type used for synthesis (male or female)")