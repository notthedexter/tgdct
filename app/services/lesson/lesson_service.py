from app.services.lesson.lesson_schema import ChapterListResponse, ChapterInfoRequest, ChapterInfoResponse


class LessonService:
    """Main lesson service that routes to different chapter services"""
    
    def __init__(self):
        self.available_chapters = [1, 2, 3, 4]  # Expandable as more chapters are added
        self.chapter_info = {
            1: {
                "title": "Introduction to Language Basics",
                "level": "A1",
                "module_count": 10
            },
            2: {
                "title": "Action, Time and Place",
                "level": "A1 → A2",
                "module_count": 7
            },
            3: {
                "title": "Family and Relationships",
                "level": "A2 → B1",
                "module_count": 3
            },
            4: {
                "title": "Expressing Gratitude and Apologies",
                "level": "B1 → B2",
                "module_count": 3
            }
        }
    
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
    
    def get_chapter_info(self, request: ChapterInfoRequest) -> ChapterInfoResponse:
        """Get information about a specific chapter"""
        chapter_number = request.chapter_number
        
        if chapter_number not in self.available_chapters:
            return ChapterInfoResponse(
                success=False,
                message=f"Chapter {chapter_number} is not available. Available chapters: {self.available_chapters}"
            )
        
        info = self.chapter_info.get(chapter_number)
        if not info:
            return ChapterInfoResponse(
                success=False,
                message=f"Chapter {chapter_number} information not found"
            )
        
        return ChapterInfoResponse(
            success=True,
            message=f"Successfully retrieved information for Chapter {chapter_number}",
            chapter_number=chapter_number,
            title=info["title"],
            level=info["level"],
            module_count=info["module_count"]
        )
