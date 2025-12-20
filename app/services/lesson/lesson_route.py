from fastapi import APIRouter, HTTPException
from app.services.lesson.lesson_service import LessonService
from app.services.lesson.lesson_schema import ChapterListResponse
from app.services.lesson.chapters.chapter1.chapter1_route import router as chapter1_router


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


# Include chapter-specific routers
router.include_router(chapter1_router, prefix="/chapter1", tags=["Chapter 1"])
