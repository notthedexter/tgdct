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
    Synthesize speech from text using gTTS.

    Args:
        request: TextToSpeechRequest with language and text

    Returns:
        Audio file in MP3 format
    """
    try:
        # Validate language
        if request.language not in ["en-US", "tl-PH"]:
            raise HTTPException(
                status_code=400,
                detail="Unsupported language. Use: en-US or tl-PH"
            )

        # Validate text
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        # Synthesize speech and get audio bytes
        audio_bytes = tts_service.synthesize_speech(
            text=request.text,
            language=request.language
        )

        # Return audio as MP3 file
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