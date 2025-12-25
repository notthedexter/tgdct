"""Dialogue builder routes."""
from fastapi import APIRouter, HTTPException
from .dialogue_service import dialogue_builder_service
from .dialogue_schema import DialogueRequest, DialogueQuestion, AnswerEvaluation
from app.core.config import settings

router = APIRouter(prefix="/dialogue", tags=["Dialogue Builder"])


@router.post("/generate-dialogue")
async def generate_dialogue(request: DialogueRequest):
    """Generate a grammar-focused dialogue based on the scenario."""
    try:
        if request.language not in settings.supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(settings.supported_languages.keys())}"
            )
        dialogue = await dialogue_builder_service.generate_dialogue(request.scenario, request.language)
        return dialogue
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluate-answer")
async def evaluate_answer(question: DialogueQuestion, selected_option_index: int):
    """Evaluate if the selected answer is correct."""
    try:
        if selected_option_index < 0 or selected_option_index >= len(question.options):
            raise HTTPException(status_code=400, detail="Invalid option index")

        evaluation = dialogue_builder_service.evaluate_answer(question, selected_option_index)
        return evaluation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
