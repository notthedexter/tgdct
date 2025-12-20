from app.services.lesson.lesson_schema import ChapterListResponse


class LessonService:
    """Main lesson service that routes to different chapter services"""
    
    def __init__(self):
        self.available_chapters = [1]  # Expandable as more chapters are added
    
    def get_available_chapters(self) -> ChapterListResponse:
        """Get list of available chapters"""
        return ChapterListResponse(
            available_chapters=self.available_chapters,
            total_chapters=len(self.available_chapters),
            description="Currently available language learning chapters"
        )
    
    def is_chapter_available(self, chapter_number: int) -> bool:
        """Check if a chapter is available"""
        return chapter_number in self.available_chapters
