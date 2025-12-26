"""Text-to-Speech service using gTTS for English and Tagalog."""
from gtts import gTTS
import io
import os
from pathlib import Path
from datetime import datetime


class TTSService:
    """Text-to-Speech service using Google Text-to-Speech."""

    def __init__(self):
        """Initialize the TTS service."""
        self.audio_dir = Path(__file__).parent / "tts_audio"
        self.audio_dir.mkdir(exist_ok=True)

    def synthesize_speech(self, text: str, language: str = "tl-PH") -> bytes:
        """
        Synthesize speech from text using gTTS.

        Args:
            text: Text to convert to speech
            language: Language code (en-US for English, tl-PH for Tagalog)

        Returns:
            Audio bytes in MP3 format
        """
        # Map language codes to gTTS language codes
        lang_map = {
            "en-US": "en",
            "tl-PH": "tl"
        }

        gtts_lang = lang_map.get(language, "tl")

        # Create gTTS object
        if gtts_lang == "tl":
            # Use Philippine TLD for better Tagalog pronunciation
            tts = gTTS(text=text, lang=gtts_lang, tld='com.ph', slow=False)
        else:
            tts = gTTS(text=text, lang=gtts_lang, slow=False)

        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        temp_filename = f"tts_{timestamp}.wav"
        temp_file_path = self.audio_dir / temp_filename

        try:
            # Save to temporary file
            tts.save(str(temp_file_path))

            # Read the file content
            with open(temp_file_path, 'rb') as f:
                audio_bytes = f.read()

            return audio_bytes

        finally:
            # Clean up temporary file
            if temp_file_path.exists():
                try:
                    os.remove(temp_file_path)
                except OSError:
                    pass  # Ignore cleanup errors


# Create singleton instance
tts_service = TTSService()


