"""Chapter 2 Router - Action, Time and Place (A1 → A2)"""
from fastapi import APIRouter, HTTPException
from app.services.lesson.chapters.chapter2.chapter2_service import Chapter2Service
from app.services.lesson.chapters.chapter2.chapter2_schema import (
    Chapter2GenerationRequest,
    Chapter2Response,
    ModuleTitlesRequest,
    ModuleTitlesResponse
)

router = APIRouter()
chapter2_service = Chapter2Service()


@router.post(
    "/titles",
    response_model=ModuleTitlesResponse,
    summary="Get Chapter 2 Module Titles in Target Language",
    description="Get all 7 module titles for Chapter 2 translated to the target language"
)
async def get_module_titles(request: ModuleTitlesRequest):
    """
    Get all Chapter 2 module titles translated to your target language.
    
    This endpoint helps you discover what modules are available in the language you're learning.
    
    **Chapter 2 Theme:** Action, Time and Place (A1 → A2 Level)
    
    **Parameters:**
    - `target_language`: Language code (e.g., "es-ES" for Spanish, "fr-FR" for French, "tl-PH" for Tagalog)
    
    **Returns:**
    - Dictionary mapping module numbers (1-7) to translated titles
    
    **Example Request:**
    ```json
    {
      "target_language": "es-ES"
    }
    ```
    
    **Example Response:**
    ```json
    {
      "success": true,
      "message": "Successfully retrieved module titles for es-ES",
      "titles": {
        "1": "Lugares y Ubicaciones",
        "2": "Sentimientos Básicos",
        "3": "Expresando Afecto (Edición Avanzada)",
        ...
      }
    }
    ```
    """
    try:
        result = await chapter2_service.get_module_titles(request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.message)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/generate",
    response_model=Chapter2Response,
    summary="Generate Chapter 2 Modules",
    description="Generate specific modules or all modules of Chapter 2 using module titles in the target language"
)
async def generate_chapter2(request: Chapter2GenerationRequest):
    """
    Generate Chapter 2 curriculum modules using titles in the language you're learning.
    
    **Chapter 2 Theme:** Action, Time and Place (A1 → A2 Level)
    
    **Workflow:**
    1. First, call `/titles` endpoint to get available module titles in your target language
    2. Then use those titles (or similar) in this endpoint to generate specific modules
    
    **Parameters:**
    - `target_language`: Language code (e.g., "es-ES", "fr-FR", "tl-PH")
    - `module_titles`: Optional list of module titles in the target language
      - If not provided, generates all 7 modules
      - If provided, generates only matching modules
      - Uses fuzzy matching, so exact spelling is not required
    
    **Example 1 - Generate all modules:**
    ```json
    {
      "target_language": "es-ES"
    }
    ```
    
    **Example 2 - Generate specific modules by title:**
    ```json
    {
      "target_language": "es-ES",
      "module_titles": ["Lugares y Ubicaciones", "Sentimientos Básicos"]
    }
    ```
    
    **Returns:**
    - Generated modules with vocabulary (10 items each) and grammar concepts
    - Each vocabulary item contains English and target language translations
    - Each grammar concept includes topic, explanation, and examples
    """
    try:
        result = await chapter2_service.generate(request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.message)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
