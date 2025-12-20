"""Chapter 1 Router - Merged single API"""
from fastapi import APIRouter, HTTPException
from app.services.lesson.chapters.chapter1.chapter1_service import Chapter1Service
from app.services.lesson.chapters.chapter1.chapter1_schema import (
    Chapter1GenerationRequest,
    Chapter1Response,
    ModuleTitlesRequest,
    ModuleTitlesResponse
)

router = APIRouter()
chapter1_service = Chapter1Service()


@router.post(
    "/titles",
    response_model=ModuleTitlesResponse,
    summary="Get Module Titles in Target Language",
    description="Get all 10 module titles translated to the target language"
)
async def get_module_titles(request: ModuleTitlesRequest):
    """
    Get all Chapter 1 module titles translated to your target language.
    
    This endpoint helps you discover what modules are available in the language you're learning.
    
    **Parameters:**
    - `target_language`: Language code (e.g., "es-ES" for Spanish, "fr-FR" for French, "tl-PH" for Tagalog)
    
    **Returns:**
    - Dictionary mapping module numbers (1-10) to translated titles
    
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
        "1": "Saludos Esenciales",
        "2": "Presentaciones Personales",
        "3": "Pertenencias",
        "4": "Familia y Relaciones",
        ...
      }
    }
    ```
    """
    try:
        result = await chapter1_service.get_module_titles(request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.message)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/generate",
    response_model=Chapter1Response,
    summary="Generate Chapter 1 Modules",
    description="Generate specific modules or all modules of Chapter 1 using module titles in the target language"
)
async def generate_chapter1(request: Chapter1GenerationRequest):
    """
    Generate Chapter 1 curriculum modules using titles in the language you're learning.
    
    **Workflow:**
    1. First, call `/titles` endpoint to get available module titles in your target language
    2. Then use those titles (or similar) in this endpoint to generate specific modules
    
    **Parameters:**
    - `target_language`: Language code (e.g., "es-ES", "fr-FR", "tl-PH")
    - `module_titles`: Optional list of module titles in the target language
      - If not provided, generates all 10 modules
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
      "module_titles": ["Saludos Esenciales", "Familia y Relaciones"]
    }
    ```
    
    **Example 3 - Fuzzy matching works:**
    ```json
    {
      "target_language": "es-ES",
      "module_titles": ["sobre familia", "colores"]
    }
    ```
    
    Each module contains vocabulary (10 items) and grammar concepts.
    """
    try:
        result = await chapter1_service.generate(request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.message)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
