from fastapi import APIRouter, HTTPException
from app.services.lesson.lesson_service import LessonService
from app.services.lesson.lesson_schema import ChapterListResponse, ChapterInfoRequest, ChapterInfoResponse
from app.services.lesson.chapters.chapter1.chapter1_route import router as chapter1_router
from app.services.lesson.chapters.chapter2.chapter2_route import router as chapter2_router
from app.services.lesson.chapters.chapter3.chapter3_route import router as chapter3_router
from app.services.lesson.chapters.chapter4.chapter4_route import router as chapter4_router


router = APIRouter(prefix="/lesson", tags=["Language Learning"])
lesson_service = LessonService()


@router.get(
    "/chapters",
    response_model=ChapterListResponse,
    summary="List Available Chapters"
)
async def list_chapters():
    """Get a list of all available chapters"""
    return lesson_service.get_available_chapters()


@router.post(
    "/chapter/info",
    response_model=ChapterInfoResponse,
    summary="Get Chapter Information",
    description="Get detailed information about a specific chapter by its number"
)
async def get_chapter_info(request: ChapterInfoRequest):
    """
    Get information about a specific chapter.
    
    **Parameters:**
    - `chapter_number`: The chapter number (e.g., 1, 2, 3)
    
    **Returns:**
    - Chapter number, title, level, and module count
    
    **Example Request:**
    ```json
    {
      "chapter_number": 3
    }
    ```
    
    **Example Response:**
    ```json
    {
      "success": true,
      "message": "Successfully retrieved information for Chapter 3",
      "chapter_number": 3,
      "title": "Family and Relationships",
      "level": "A2 → B1",
      "module_count": 3
    }
    ```
    """
    try:
        result = lesson_service.get_chapter_info(request)
        
        if not result.success:
            raise HTTPException(status_code=404, detail=result.message)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Include chapter-specific routers
router.include_router(chapter1_router, prefix="/chapter1", tags=["Chapter 1"])
router.include_router(chapter2_router, prefix="/chapter2", tags=["Chapter 2"])
router.include_router(chapter3_router, prefix="/chapter3", tags=["Chapter 3"])
router.include_router(chapter4_router, prefix="/chapter4", tags=["Chapter 4"])
