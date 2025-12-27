"""Pydantic models for conversation roleplay service."""
from pydantic import BaseModel, Field
from typing import List, Optional


class ConversationStartRequest(BaseModel):
    """Request model for starting a new conversation."""
    language: str = Field(default="en-US", description="Language code for the conversation")


class ConversationStartResponse(BaseModel):
    """Response model for conversation start."""
    conversation_id: str  # Unique ID for this conversation
    ai_message: str  # AI's opening message in target language  

class ConversationReplyRequest(BaseModel):
    """Request model for replying to the conversation."""
    conversation_id: str  # The conversation ID
    user_message: str  # User's response in the target language
    language: str = Field(default="en-US", description="Language code")


class ConversationReplyResponse(BaseModel):
    """Response model for AI's reply."""
    ai_message: str  # AI's reply in target language

    conversation_ended: bool = False  # Whether conversation has naturally ended
