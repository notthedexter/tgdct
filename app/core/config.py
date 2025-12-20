"""Application configuration and settings."""
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import HTTPException

# Load .env file from project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application settings and configuration."""
    
    def __init__(self):
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY")
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        self.app_title = "Language Learning Platform"
        self.app_description = "Speech-to-Text and Writing Practice using AI"
        self.host = "127.0.0.1"
        self.port = 8054
        self.stt_model = "gemini-2.5-flash"
        self.tts_model = "gemini-2.5-flash-tts"
        self.writing_model = "llama-3.3-70b-versatile"
        self.default_language = "en-US"  # English by default
        self.supported_languages = {
            
            "en-US": "English",
            "es-ES": "Spanish",
            "fr-FR": "French",
            "de-DE": "German",
            "it-IT": "Italian",
            "pt-BR": "Portuguese",
            "ja-JP": "Japanese",
            "ko-KR": "Korean",
            "zh-CN": "Mandarin Chinese",
            "ru-RU": "Russian",
            "ar-SA": "Arabic",
            "tl-PH": "Tagalog",
            "hi-IN": "Hindi",
            "th-TH": "Thai",
            "vi-VN": "Vietnamese",
            "nl-NL": "Dutch",
            "pl-PL": "Polish",
            "tr-TR": "Turkish",
            "sv-SE": "Swedish",
            "no-NO": "Norwegian"
        }
    
    def get_api_key(self) -> str:
        """Get the Gemini API key, raise exception if not set."""
        if not self.gemini_api_key:
            raise HTTPException(
                status_code=500,
                detail="GEMINI_API_KEY environment variable not set"
            )
        return self.gemini_api_key
    
    def get_groq_api_key(self) -> str:
        """Get the Groq API key, raise exception if not set."""
        if not self.groq_api_key:
            raise HTTPException(
                status_code=500,
                detail="GROQ_API_KEY environment variable not set"
            )
        return self.groq_api_key


# Global settings instance
settings = Settings()
