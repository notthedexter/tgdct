"""STT API routes and endpoints."""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from app.services.stt.stt_schema import SpeechToTextResponse
from app.services.stt.stt_service import stt_service
from app.core.config import settings


router = APIRouter(prefix="", tags=["Speech-to-Text"])


@router.post("/transcribe", response_model=SpeechToTextResponse)
async def transcribe_speech(
    audio_file: UploadFile = File(...),
    language: str = Form(default="en-US")
):
    """
    Transcribe speech from audio file to text using Gemini API.
    
    Args:
        audio_file: Audio file to transcribe
        language: Target language for transcription (BCP-47 code)
        
    Returns:
        SpeechToTextResponse with transcribed text
    """
    try:
        # Validate language
        if language not in settings.supported_languages:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported language. Use: {', '.join(settings.supported_languages.keys())}"
            )
        
        # Read audio file
        audio_data = await audio_file.read()
        
        if not audio_data:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        # Transcribe audio
        result = stt_service.transcribe_audio(
            audio_data=audio_data,
            language=language
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
