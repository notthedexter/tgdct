# """Text-to-Speech service implementation."""
# import random
# import os
# import base64
# from datetime import datetime
# from pathlib import Path
# from google import genai
# from google.genai import types
# from fastapi import HTTPException

# from app.core.config import settings
# from app.services.tts.tts_schema import TextToSpeechResponse


# class TTSService:
#     """Text-to-Speech service using Google Gemini API."""

#     def __init__(self):
#         """Initialize the TTS service."""
#         self.model = "gemini-2.5-flash-preview-tts"  # Use the specific TTS model
#         # Available voices with their types
#         self.voices = [
#             {"name": "Puck", "type": "female"},
#             {"name": "Charon", "type": "male"},
#             {"name": "Kore", "type": "female"},
#             {"name": "Fenrir", "type": "male"},
#             {"name": "Aoede", "type": "female"}
#         ]
#         # Create tts directory if it doesn't exist
#         self.tts_dir = Path(__file__).parent / "tts_audio"
#         self.tts_dir.mkdir(exist_ok=True)

#     def synthesize_speech(
#         self,
#         text: str,
#         language: str = "en-US"
#     ) -> TextToSpeechResponse:
#         """
#         Synthesize speech from text using Google Gemini API.

#         Args:
#             text: Text to convert to speech
#             language: Language for speech synthesis (BCP-47 code)

#         Returns:
#             TextToSpeechResponse with audio data

#         Raises:
#             HTTPException: If synthesis fails
#         """
#         # Randomly select a voice
#         selected_voice_info = random.choice(self.voices)
#         selected_voice_name = selected_voice_info["name"]
#         selected_voice_type = selected_voice_info["type"]

#         # Get API key from settings
#         api_key = settings.get_api_key()
#         client = genai.Client(api_key=api_key)

#         try:
#             # Prepare the content with clear TTS instruction
#             contents = types.Content(
#                 role="user",
#                 parts=[types.Part.from_text(text=text)]
#             )
            
#             # Generate speech using Gemini TTS model with speech configuration
#             response = client.models.generate_content(
#                 model=self.model,
#                 contents=contents,
#                 config=types.GenerateContentConfig(
#                     response_modalities=["AUDIO"],
#                     speech_config=types.SpeechConfig(
#                         voice_config=types.VoiceConfig(
#                             prebuilt_voice_config=types.PrebuiltVoiceConfig(
#                                 voice_name=selected_voice_name
#                             )
#                         )
#                     ),
#                     system_instruction="You are a text-to-speech system. Convert the provided text into speech audio. Do not generate any text response."
#                 )
#             )

#             # Extract audio data from response
#             if not response or not response.candidates:
#                 raise HTTPException(
#                     status_code=500,
#                     detail="No audio generated"
#                 )

#             # Get the audio data from the response
#             candidate = response.candidates[0]
#             audio_data = None
            
#             if candidate.content and candidate.content.parts:
#                 for part in candidate.content.parts:
#                     if hasattr(part, 'inline_data') and part.inline_data:
#                         audio_data = part.inline_data.data
#                         break

#             if not audio_data:
#                 raise HTTPException(
#                     status_code=500,
#                     detail="No audio data in response"
#                 )

#             # Decode base64 audio data if it's encoded
#             if isinstance(audio_data, str):
#                 audio_bytes = base64.b64decode(audio_data)
#             else:
#                 audio_bytes = audio_data

#             # Generate unique filename with timestamp
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
#             filename = f"tts_{timestamp}.wav"
#             file_path = self.tts_dir / filename

#             # Save audio file
#             with open(file_path, "wb") as f:
#                 f.write(audio_bytes)

#             # Get relative path for response
#             relative_path = f"app/services/tts/tts_audio/{filename}"

#             return TextToSpeechResponse(
#                 file_location=relative_path,
#                 voice=selected_voice_type
#             )

#         except HTTPException:
#             raise
#         except Exception as e:
#             raise HTTPException(
#                 status_code=500,
#                 detail=f"Speech synthesis failed: {str(e)}"
#             )


# # Global service instance
# tts_service = TTSService()