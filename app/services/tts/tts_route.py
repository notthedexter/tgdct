"""TTS API routes and endpoints."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.services.tts.tts_schema import TextToSpeechRequest
from app.services.tts.tts_service import tts_service
from app.core.config import settings


router = APIRouter(prefix="", tags=["Text-to-Speech"])


@router.post("/synthesize")
async def synthesize_speech(request: TextToSpeechRequest):
    """
    Synthesize speech from text using Hugging Face TTS model.

    Args:
        request: TextToSpeechRequest with text and options

    Returns:
        Audio file in WAV format
    """
    try:
        # Validate language (only tl-PH supported)
        if request.language not in ["tl-PH", "en-US"]:
            raise HTTPException(
                status_code=400,
                detail="Unsupported language. Use: tl-PH"
            )

        # Validate text
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        # Synthesize speech and get audio bytes
        audio_bytes = tts_service.synthesize_speech(
            text=request.text,
            language=request.language
        )

        # Return audio as WAV file
        return Response(
            content=audio_bytes,
            media_type="audio/wav",
            headers={
                "Content-Disposition": "attachment; filename=speech.wav"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))