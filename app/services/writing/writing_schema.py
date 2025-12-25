"""Pydantic models for writing practice service."""
from pydantic import BaseModel
from typing import List


class PromptResponse(BaseModel):
    """Response model for prompt generation."""
    prompt: str
    
    
class EvaluationRequest(BaseModel):
    """Request model for evaluating user response."""
    prompt: str
    user_response: str
    language: str = "en-US"
    

class EvaluationResponse(BaseModel):
    """Response model for evaluation."""
    rating: str  # excellent, good, or need to improve
    need_to_improve: bool  # false if excellent, true otherwise
    sample_response: str  # example good response to the prompt
