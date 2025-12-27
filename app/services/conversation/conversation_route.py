"""Conversation roleplay routes."""
from fastapi import APIRouter, HTTPException, Query
from .conversation_service import conversation_service
from .conversation_schema import ConversationStartRequest, ConversationReplyRequest
from app.core.config import settings

router = APIRouter(prefix="/conversation", tags=["Sequential Conversation Practice"])


@router.post("/start")
async def start_conversation(
    language: str = Query(default="en-US", description="Language for the conversation")
):
    """Start a sequential conversation practice. AI will say the first phrase for you to repeat."""
    try:
        if language not in settings.supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(settings.supported_languages.keys())}"
            )
        result = await conversation_service.start_conversation(language)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reply")
async def reply_to_conversation(request: ConversationReplyRequest):
    """Repeat the phrase. AI will verify and continue with the next phrase in the conversation."""
    try:
        if request.language not in settings.supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(settings.supported_languages.keys())}"
            )
        result = await conversation_service.reply_to_conversation(
            conversation_id=request.conversation_id,
            user_message=request.user_message,
            language=request.language
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
