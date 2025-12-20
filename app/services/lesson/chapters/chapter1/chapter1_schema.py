"""Chapter 1 schemas - Merged single API"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class ModuleNumber(int, Enum):
    """Module numbers with their names"""
    MODULE_1_GREETINGS = 1
    MODULE_2_SELF_INTRO = 2
    MODULE_3_BELONGINGS = 3
    MODULE_4_FAMILY = 4
    MODULE_5_LIKES_DISLIKES = 5
    MODULE_6_GRATITUDE = 6
    MODULE_7_NUMBERS_1_10 = 7
    MODULE_8_NUMBERS_11_100 = 8
    MODULE_9_COLORS = 9
    MODULE_10_REVIEW = 10


MODULE_NAMES = {
    1: "Essential Greetings",
    2: "Self Introductions",
    3: "Belongings",
    4: "Family & Relationships",
    5: "Basic Likes/Dislikes",
    6: "Gratitude & Apologies",
    7: "Numbers 1-10",
    8: "Numbers 11-100",
    9: "Colors",
    10: "Review & Integration"
}


class VocabularyItem(BaseModel):
    """Individual vocabulary item"""
    number: int = Field(..., description="Item number (1-10)")
    english: str = Field(..., description="English word/phrase")
    target: str = Field(..., description="Translation in target language")


class GrammarConcept(BaseModel):
    """Grammar explanation for the module"""
    topic: str = Field(..., description="Grammar topic name")
    requirement: str = Field(..., description="Explanation of the grammar rule")
    examples: List[str] = Field(default_factory=list, description="Example sentences")


class ModuleContent(BaseModel):
    """Content for a single module"""
    module_number: int = Field(..., description="Module number (1-10)")
    title: str = Field(..., description="Module title")
    vocabulary: List[VocabularyItem] = Field(..., min_items=10, max_items=10)
    grammar: GrammarConcept


class ModuleTitlesRequest(BaseModel):
    """Request to get module titles in target language"""
    target_language: str = Field(..., description="Target language code (e.g., es-ES, fr-FR, tl-PH)")


class ModuleTitlesResponse(BaseModel):
    """Response with module titles in target language"""
    success: bool
    message: str
    titles: Optional[Dict[int, str]] = Field(default=None, description="Module number to translated title mapping")


class Chapter1GenerationRequest(BaseModel):
    """Request to generate Chapter 1 modules"""
    target_language: str = Field(..., description="Target language code (e.g., es-ES, fr-FR, tl-PH)")
    module_titles: Optional[List[str]] = Field(
        default=None,
        description="Module titles in the target language. If not provided, generates all modules.",
        example=["Saludos Esenciales", "Sobre Familia"]
    )


class Chapter1Content(BaseModel):
    """Chapter 1 with requested modules"""
    modules: List[ModuleContent] = Field(..., min_items=1, max_items=10, description="Requested modules")


class Chapter1Response(BaseModel):
    """Response for Chapter 1 generation"""
    success: bool
    message: str
    chapter: Optional[Chapter1Content] = None
    generation_info: Optional[Dict[str, Any]] = None
