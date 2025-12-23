"""Chapter 2 schemas - Action, Time and Place (A1 → A2)"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class ModuleNumber(int, Enum):
    """Module numbers with their names"""
    MODULE_1_PLACES = 1
    MODULE_2_BASIC_FEELINGS = 2
    MODULE_3_AFFECTION = 3
    MODULE_4_SURPRISES = 4
    MODULE_5_TIME = 5
    MODULE_6_MONTHS = 6
    MODULE_7_DAYS = 7


MODULE_NAMES = {
    1: "Places and Locations",
    2: "Basic Feelings",
    3: "Expressing Affection (Advanced Edition)",
    4: "Expressing Surprises and Reactions",
    5: "Time and Telling Time",
    6: "Months of the Year",
    7: "Days of the Week"
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
    module_number: int = Field(..., description="Module number (1-7)")
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


class Chapter2GenerationRequest(BaseModel):
    """Request to generate Chapter 2 modules"""
    target_language: str = Field(..., description="Target language code (e.g., es-ES, fr-FR, tl-PH)")
    module_titles: Optional[List[str]] = Field(
        default=None,
        description="Module titles in the target language. If not provided, generates all modules.",
        example=["Lugares y Ubicaciones", "Sentimientos Básicos"]
    )


class Chapter2Content(BaseModel):
    """Chapter 2 with requested modules"""
    modules: List[ModuleContent] = Field(..., min_items=1, max_items=7, description="Requested modules")


class Chapter2Response(BaseModel):
    """Response for Chapter 2 generation"""
    success: bool
    message: str
    chapter: Optional[Chapter2Content] = None
    generation_info: Optional[Dict[str, Any]] = None
