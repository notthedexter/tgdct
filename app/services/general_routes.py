"""Routes for general app information and health checks."""
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(prefix="", tags=["General"])


@router.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_title,
        "description": settings.app_description,
        "version": "2.0.0",
        "endpoints": {
            "languages": "/languages",
            "transcribe": "/transcribe",
            "writing": "/writing",
            "dictionary": "/dictionary",
            "flashcards": "/flashcards",
            "roleplay": "/roleplay"
        }
    }


@router.get("/languages")
async def get_supported_languages():
    """Get list of supported languages for learning."""
    return {
        "default_language": settings.default_language,
        "supported_languages": settings.supported_languages,
        "total_languages": len(settings.supported_languages)
    }
