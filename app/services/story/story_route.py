"""AI story routes."""
from fastapi import APIRouter, HTTPException
from .story_service import ai_story_service
from .story_schema import StoryRequest
from app.core.config import settings

router = APIRouter(prefix="/story", tags=["AI Story"])


@router.post("/generate-story")
async def generate_story(request: StoryRequest):
    """Generate a short story (7-8 lines maximum) based on the topic."""
    try:
        if request.language not in settings.supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(settings.supported_languages.keys())}"
            )
        story = await ai_story_service.generate_story(request.topic, request.language)
        return story
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))