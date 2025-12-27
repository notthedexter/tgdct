"""FastAPI application entry point."""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.services.general_routes import router as general_router
from app.services.stt.stt_route import router as stt_router
from app.services.tts.tts_route import router as tts_router
from app.services.writing.writing_route import router as writing_router
from app.services.dictionary.dictionary_route import router as dictionary_router
from app.services.flashcards.flashcards_route import router as flashcards_router
from app.services.roleplay.roleplay_route import router as roleplay_router
from app.services.dialogue.dialogue_route import router as dialogue_router
from app.services.listening.listening_route import router as listening_router
from app.services.story.story_route import router as story_router
from app.services.conversation.conversation_route import router as conversation_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.app_title,
        description=settings.app_description
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify your domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    
    app.include_router(general_router)
    app.include_router(stt_router)
    app.include_router(tts_router)
    app.include_router(flashcards_router)
    app.include_router(conversation_router)
    app.include_router(listening_router)
    app.include_router(writing_router)
    app.include_router(dictionary_router)
    app.include_router(story_router)
    app.include_router(dialogue_router)
    app.include_router(roleplay_router)
    
    
    
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
