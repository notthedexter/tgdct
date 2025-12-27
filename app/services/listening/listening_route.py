"""Listening practice routes."""
from fastapi import APIRouter, HTTPException
from .listening_service import listening_practice_service
from .listening_schema import ListeningRequest, ListeningQuestion, ListeningAnswerEvaluation
from app.core.config import settings

router = APIRouter(prefix="/listening", tags=["Listening Practice"])


@router.post("/generate-practice")
async def generate_listening_practice(request: ListeningRequest):
    """Generate 5 listening practice questions based on the topic."""
    try:
        if request.language not in settings.supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(settings.supported_languages.keys())}"
            )
        practice = await listening_practice_service.generate_listening_practice(request.topic, request.language)
        return practice
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



