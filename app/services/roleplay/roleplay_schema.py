"""Pydantic models for AI roleplay service."""
from pydantic import BaseModel, Field
from typing import Optional


class RoleplayScenarioRequest(BaseModel):
    """Request model for generating a roleplay scenario."""
    pass  # No parameters needed, generates automatically


class RoleplayScenarioResponse(BaseModel):
    """Response model for roleplay scenario generation."""
    scenario: str  # English description of the scenario
    question_in_language: str  # Question in the target language
    question_english: str  # Question in English
    language: str  # The language code used


class RoleplayResponseRequest(BaseModel):
    """Request model for evaluating a roleplay response."""
    scenario: str  # The scenario description
    question_in_language: str  # The question in the target language
    question_english: str  # The question in English
    user_response: str  # User's response in the target language
    language: str = Field(default="en-US", description="Language code of the response")


class RoleplayResponseEvaluation(BaseModel):
    """Response model for roleplay response evaluation."""
    needs_improvement: bool
    original: Optional[str] = None  # Original response if improvement needed
    better: Optional[str] = None  # Improved version in the target language if needed