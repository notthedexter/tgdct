"""Speech-to-Text service implementation."""
from google import genai
from google.genai import types
from fastapi import HTTPException

from app.core.config import settings
from app.services.stt.stt_schema import SpeechToTextResponse


class STTService:
    """Speech-to-Text service using Google Gemini API."""
    
    def __init__(self):
        """Initialize the STT service."""
        self.model = settings.stt_model
    
    def transcribe_audio(
        self, 
        audio_data: bytes,
        language: str = "en-US"
    ) -> SpeechToTextResponse:
        """
        Transcribe audio to text using Google Gemini API.
        
        Args:
            audio_data: Audio file data as bytes
            language: Target language for transcription (BCP-47 code)
            
        Returns:
            SpeechToTextResponse with transcribed text
            
        Raises:
            HTTPException: If transcription fails
        """
        # Get API key from settings
        api_key = settings.get_api_key()
        client = genai.Client(api_key=api_key)

        # Determine MIME type (WebM for browser recordings)
        mime_type = 'audio/webm'

        # Prepare language-specific prompt
        language_name = settings.supported_languages.get(language, "Tagalog")
        prompt = f"Transcribe this audio in {language_name}. Provide only the transcribed text without any additional commentary."
        
        # Prepare content with audio
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                    types.Part.from_bytes(
                        data=audio_data,
                        mime_type=mime_type
                    )
                ],
            ),
        ]

        try:
            # Generate transcription
            response = client.models.generate_content(
                model=self.model,
                contents=contents,
            )
            
            # Extract transcribed text
            if not response or not response.text:
                raise HTTPException(
                    status_code=500, 
                    detail="No transcription generated"
                )
            
            transcribed_text = response.text.strip()
            
            return SpeechToTextResponse(
                text=transcribed_text,
                language=language,
                detected_language=language
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Transcription failed: {str(e)}"
            )


# Global service instance
stt_service = STTService()
