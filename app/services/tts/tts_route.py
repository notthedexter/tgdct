"""TTS API routes and endpoints."""
from fastapi import APIRouter, HTTPException

from app.services.tts.tts_schema import TextToSpeechRequest, TextToSpeechResponse
from app.services.tts.tts_service import tts_service
from app.core.config import settings


router = APIRouter(prefix="", tags=["Text-to-Speech"])


@router.post("/synthesize", response_model=TextToSpeechResponse)
async def synthesize_speech(request: TextToSpeechRequest):
    """
    Synthesize speech from text using Gemini API.

    Args:
        request: TextToSpeechRequest with text and options

    Returns:
        StreamingResponse with audio data
    """
    try:
        # Validate language
        if request.language not in settings.supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Use: {', '.join(settings.supported_languages.keys())}"
            )

        # Validate text
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        # Synthesize speech and save to file
        result = tts_service.synthesize_speech(
            text=request.text,
            language=request.language
        )

        # Return file location and voice type
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))