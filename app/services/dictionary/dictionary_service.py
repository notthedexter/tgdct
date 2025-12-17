"""Dictionary service using Gemini API."""
import google.genai as genai
from google.genai import types
from fastapi import UploadFile
from app.core.config import settings
from .dictionary_schema import TextSearchResponse
import json
import re


class DictionaryService:
    """Service for image detection and text dictionary search."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        self.gemini_client = genai.Client(api_key=settings.get_api_key())
    
    def detect_object_in_image(self, image_file: UploadFile, language: str = "en-US") -> TextSearchResponse:
        """Detect object in image and return its name in the specified language with dictionary information.
        
        Args:
            image_file: UploadFile object containing the image
            language: Target language code (e.g., tl-PH, es-ES, fr-FR)
            
        Returns:
            TextSearchResponse with detected word in the target language and its dictionary information
        """
        # Determine mime type based on filename
        filename = image_file.filename.lower()
        if filename.endswith('.jpg') or filename.endswith('.jpeg'):
            mime_type = "image/jpeg"
        elif filename.endswith('.png'):
            mime_type = "image/png"
        elif filename.endswith('.webp'):
            mime_type = "image/webp"
        elif filename.endswith('.gif'):
            mime_type = "image/gif"
        else:
            # Default to jpeg if extension not recognized
            mime_type = "image/jpeg"
        
        # Read image data
        image_data = image_file.file.read()
        
        language_name = settings.supported_languages.get(language, "the target language")
        
        prompt = f"""Look at this image and identify the main object or word shown.
Provide ONE word for the main object in {language_name}. Return only the word, nothing else."""
        
        response = self.gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part(text=prompt),
                        types.Part(inline_data=types.Blob(mime_type=mime_type, data=image_data))
                    ]
                )
            ]
        )
        
        word_in_language = response.text.strip()
        return self.search_word(word_in_language, language)
    
    def search_word(self, word: str, language: str = "en-US") -> TextSearchResponse:
        """Search for a word in the specified language and get detailed information.
        
        Args:
            word: Word to search in the target language
            language: Language code (e.g., tl-PH, es-ES, fr-FR)
            
        Returns:
            TextSearchResponse with syllables, meanings, and example sentences
        """
        language_name = settings.supported_languages.get(language, "the target language")
        
        system_prompt = f"""You are a {language_name}-English dictionary expert.

When given a {language_name} word, provide:
3. One example sentence in English using the word
4. One example sentence in {language_name} using the word

IMPORTANT: If the word does not exist in {language_name} or is not relatively close to any known {language_name} words, respond with this exact JSON:
{{
  "word": "No words found",
  "syllables": "",
  "meanings": [],
  "english_sentence": "",
  "sentence_in_language": "",
  "language": "{language}"
}}

Respond ONLY with valid JSON in this exact format:
{{
  "word": "original word",
  "syllables": "pronunciation-with-STRESS",
  "meanings": ["direct synonym 1", "direct synonym 2", "Descriptive explanation in one short sentence."],
  "english_sentence": "Example sentence in English",
  "sentence_in_language": "Example sentence in {language_name}",
  "language": "{language}"
}}

Be accurate and helpful."""
        
        user_message = f"Define the {language_name} word: {word}"
        
        response = self.gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_prompt}\n\n{user_message}"
        )
        
        result_text = response.text.strip()
        
        # Parse JSON response
        try:
            # Remove markdown code blocks if present
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            
            result = json.loads(result_text)
            
            # Check if no words found
            if result.get("word") == "No words found":
                return TextSearchResponse(
                    word="No words found",
                    syllables="",
                    meanings=[],
                    english_sentence="",
                    sentence_in_language="",
                    language=language
                )
            
            return TextSearchResponse(
                word=result.get("word", word),
                syllables=result.get("syllables", word),
                meanings=result.get("meanings", ["No meaning found"]),
                english_sentence=result.get("english_sentence", ""),
                sentence_in_language=result.get("sentence_in_language", ""),
                language=language
            )
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return TextSearchResponse(
                word=word,
                syllables=word,
                meanings=["Unable to find meaning"],
                english_sentence="Please try again.",
                sentence_in_language="",
                language=language
            )


# Initialize service
dictionary_service = DictionaryService()
