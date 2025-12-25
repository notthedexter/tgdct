"""Chapter 4 Router - Expressing Gratitude and Apologies (B1 → B2)"""
from fastapi import APIRouter, HTTPException
from app.services.lesson.chapters.chapter4.chapter4_service import Chapter4Service
from app.services.lesson.chapters.chapter4.chapter4_schema import (
    Chapter4GenerationRequest,
    Chapter4Response,
    ModuleTitlesRequest,
    ModuleTitlesResponse
)

router = APIRouter()
chapter4_service = Chapter4Service()


@router.post(
    "/titles",
    response_model=ModuleTitlesResponse,
    summary="Get Chapter 4 Module Titles in Target Language",
    description="Get all 3 module titles for Chapter 4 translated to the target language"
)
async def get_module_titles(request: ModuleTitlesRequest):
    """
    Get all Chapter 4 module titles translated to your target language.
    
    This endpoint helps you discover what modules are available in the language you're learning.
    
    **Chapter 4 Theme:** Expressing Gratitude and Apologies (B1 → B2 Level)
    
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
        "1": "Expresar gratitud apropiadamente",
        "2": "Disculparse formal o casualmente",
        "3": "Comprender valores culturales"
      }
    }
    ```
    """
    try:
        result = await chapter4_service.get_module_titles(request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.message)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/generate",
    response_model=Chapter4Response,
    summary="Generate Chapter 4 Modules",
    description="Generate specific modules or all modules of Chapter 4 using module titles in the target language"
)
async def generate_chapter4(request: Chapter4GenerationRequest):
    """
    Generate Chapter 4 curriculum modules using titles in the language you're learning.
    
    **Chapter 4 Theme:** Expressing Gratitude and Apologies (B1 → B2 Level)
    
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
      "module_titles": ["Expresar gratitud apropiadamente", "Comprender valores culturales"]
    }
    ```
    
    **Response includes:**
    - Module number and title
    - 10 vocabulary items (English + translation)
    - Grammar concept with explanation and examples
    
    **Note:** The API uses fuzzy matching, so you don't need exact spelling.
    For example, "expresar gratitud" will match "Expresar gratitud apropiadamente"
    """
    try:
        result = await chapter4_service.generate(request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.message)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
