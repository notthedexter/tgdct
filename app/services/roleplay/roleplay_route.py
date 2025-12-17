"""Roleplay routes."""
from fastapi import APIRouter, HTTPException, Query
from .roleplay_service import roleplay_service
from .roleplay_schema import RoleplayScenarioRequest, RoleplayResponseRequest
from app.core.config import settings

router = APIRouter(prefix="/roleplay", tags=["AI Roleplay"])


@router.post("/generate-scenario")
async def generate_scenario(
    language: str = Query(default="en-US", description="Language for the roleplay scenario")
):
    """Generate a new roleplay scenario with questions in the specified language."""
    try:
        if language not in settings.supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(settings.supported_languages.keys())}"
            )
        result = roleplay_service.generate_scenario(language)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluate-response")
async def evaluate_response(request: RoleplayResponseRequest):
    """Evaluate a user's roleplay response and provide feedback."""
    try:
        if request.language not in settings.supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(settings.supported_languages.keys())}"
            )
        result = roleplay_service.evaluate_response(
            scenario=request.scenario,
            question_in_language=request.question_in_language,
            question_english=request.question_english,
            user_response=request.user_response,
            language=request.language
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))