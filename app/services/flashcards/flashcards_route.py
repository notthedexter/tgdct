"""Flashcards routes."""
from fastapi import APIRouter, HTTPException, Query

from .flashcards_service import flashcards_service
from .flashcards_schema import FlashcardValidationRequest, FlashcardValidationResponse
from app.core.config import settings

router = APIRouter(prefix="/flashcards", tags=["Flashcards"])


@router.post("/generate")
async def generate_flashcards(
    language: str = Query(default="en-US", description="Language for flashcard generation")
):
    """Generate 5 flashcards in the specified language."""
    try:
        if language not in settings.supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(settings.supported_languages.keys())}"
            )
        result = flashcards_service.generate_flashcards(language)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate", response_model=FlashcardValidationResponse)
async def validate_flashcard(request: FlashcardValidationRequest):
    """Validate if user's response matches the correct flashcard word."""
    try:
        matches = flashcards_service.validate_flashcard(
            word=request.word,
            user_response=request.user_response
        )
        return FlashcardValidationResponse(matches=matches)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))