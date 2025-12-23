"""Chapter 3 Router - Family and Relationships (A2 → B1)"""
from fastapi import APIRouter, HTTPException
from app.services.lesson.chapters.chapter3.chapter3_service import Chapter3Service
from app.services.lesson.chapters.chapter3.chapter3_schema import (
    Chapter3GenerationRequest,
    Chapter3Response,
    ModuleTitlesRequest,
    ModuleTitlesResponse
)

router = APIRouter()
chapter3_service = Chapter3Service()


@router.post(
    "/titles",
    response_model=ModuleTitlesResponse,
    summary="Get Chapter 3 Module Titles in Target Language",
    description="Get all 3 module titles for Chapter 3 translated to the target language"
)
async def get_module_titles(request: ModuleTitlesRequest):
    """
    Get all Chapter 3 module titles translated to your target language.
    
    This endpoint helps you discover what modules are available in the language you're learning.
    
    **Chapter 3 Theme:** Family and Relationships (A2 → B1 Level)
    
    **Parameters:**
    - `target_language`: Language code (e.g., "es-ES" for Spanish, "fr-FR" for French, "tl-PH" for Tagalog)
    
    **Returns:**
    - Dictionary mapping module numbers (1-3) to translated titles
    
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
        "1": "Identificar miembros de la familia",
        "2": "Usar pronombres posesivos correctamente",
        "3": "Presentar a otras personas"
      }
    }
    ```
    """
    try:
        result = await chapter3_service.get_module_titles(request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.message)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/generate",
    response_model=Chapter3Response,
    summary="Generate Chapter 3 Modules",
    description="Generate specific modules or all modules of Chapter 3 using module titles in the target language"
)
async def generate_chapter3(request: Chapter3GenerationRequest):
    """
    Generate Chapter 3 curriculum modules using titles in the language you're learning.
    
    **Chapter 3 Theme:** Family and Relationships (A2 → B1 Level)
    
    **Workflow:**
    1. First, call `/titles` endpoint to get available module titles in your target language
    2. Then use those titles (or similar) in this endpoint to generate specific modules
    
    **Parameters:**
    - `target_language`: Language code (e.g., "es-ES", "fr-FR", "tl-PH")
    - `module_titles`: Optional list of module titles in the target language
      - If not provided, generates all 3 modules
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
      "module_titles": ["Identificar miembros de la familia", "Presentar a otras personas"]
    }
    ```
    
    **Returns:**
    - Generated modules with vocabulary (10 items each) and grammar concepts
    - Each vocabulary item contains English and target language translations
    - Each grammar concept includes topic, explanation, and examples
    """
    try:
        result = await chapter3_service.generate(request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.message)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
