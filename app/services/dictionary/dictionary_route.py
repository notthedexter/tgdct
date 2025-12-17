"""Dictionary routes."""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from .dictionary_service import dictionary_service
from app.core.config import settings

router = APIRouter(prefix="/dictionary", tags=["Dictionary"])


@router.post("/detect-image")
async def detect_image(
    image: UploadFile = File(...),
    language: str = Form(default="en-US", description="Target language for the word")
):
    """Detect object in image and return word in the specified language with dictionary information."""
    try:
        if language not in settings.supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(settings.supported_languages.keys())}"
            )
        result = dictionary_service.detect_object_in_image(image, language)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search")
async def search_word(
    word: str,
    language: str = Query(default="en-US", description="Language of the word to search")
):
    """Search for a word in the specified language dictionary."""
    try:
        if language not in settings.supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(settings.supported_languages.keys())}"
            )
        result = dictionary_service.search_word(word, language)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
