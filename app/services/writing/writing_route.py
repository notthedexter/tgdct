
from fastapi import APIRouter, HTTPException, Query
from .writing_service import writing_service
from .writing_schema import EvaluationRequest
from app.core.config import settings

router = APIRouter(prefix="/writing", tags=["Writing Practice"])


@router.post("/generate-prompt")
async def generate_prompt(
    language: str = Query(default="en-US", description="Language to practice (e.g., en-US, es-ES, fr-FR)")
):
    """Generate a new writing prompt for the specified language."""
    try:
        if language not in settings.supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(settings.supported_languages.keys())}"
            )
        prompt = await writing_service.generate_prompt(language)
        return prompt
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluate")
async def evaluate_response(request: EvaluationRequest):
    """Evaluate user's writing response."""
    try:
        evaluation = await writing_service.evaluate_response(
            request.prompt,
            request.user_response,
            request.language
        )
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))