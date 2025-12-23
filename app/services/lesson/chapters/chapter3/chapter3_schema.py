"""Chapter 3 schemas - Family and Relationships (A2 → B1)"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class ModuleNumber(int, Enum):
    """Module numbers with their names"""
    MODULE_1_FAMILY_MEMBERS = 1
    MODULE_2_POSSESSIVE_PRONOUNS = 2
    MODULE_3_INTRODUCE_PEOPLE = 3


MODULE_NAMES = {
    1: "Identify family members",
    2: "Use possessive pronouns correctly",
    3: "Introduce other people"
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
    module_number: int = Field(..., description="Module number (1-3)")
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


class Chapter3GenerationRequest(BaseModel):
    """Request to generate Chapter 3 modules"""
    target_language: str = Field(..., description="Target language code (e.g., es-ES, fr-FR, tl-PH)")
    module_titles: Optional[List[str]] = Field(
        default=None,
        description="Module titles in the target language. If not provided, generates all modules.",
        example=["Identificar miembros de la familia", "Usar pronombres posesivos correctamente"]
    )


class Chapter3Content(BaseModel):
    """Chapter 3 with requested modules"""
    modules: List[ModuleContent] = Field(..., min_items=1, max_items=3, description="Requested modules")


class Chapter3Response(BaseModel):
    """Response for Chapter 3 generation"""
    success: bool
    message: str
    chapter: Optional[Chapter3Content] = None
    generation_info: Optional[Dict[str, Any]] = None
