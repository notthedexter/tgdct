"""Flashcards service using Gemini API."""
import google.genai as genai
from app.core.config import settings
from .flashcards_schema import FlashcardItem, FlashcardResponse
import json


class FlashcardsService:
    """Service for generating Tagalog flashcards."""

    def __init__(self):
        """Initialize the Gemini client."""
        self.gemini_client = genai.Client(api_key=settings.get_api_key())

    def generate_flashcards(self, language: str = "en-US") -> FlashcardResponse:
        """Generate 5 words in the specified language with flashcard information.

        Args:
            language: Language code for flashcard generation (e.g., tl-PH, es-ES, fr-FR)

        Returns:
            FlashcardResponse with 5 flashcard items
        """
        language_name = settings.supported_languages.get(language, "the target language")
        
        system_prompt = f"""You are a {language_name} language expert creating educational flashcards.

Generate 5 different {language_name} words from various topics and subtopics. For each word, provide:

1. syllables: Pronunciation syllables separated by hyphens with the stressed syllable in UPPERCASE (e.g., "kah-MOOS-tah")
2. meaning: A brief English translation (1-2 words)
3. topic_name: A broad topic category in English (e.g., "Introduction", "Family", "Food", etc.)
4. sub_topic_name: A more specific subtopic within the topic (e.g., "Basic Greetings", "Family Members", "Fruits", etc.)
5. word: The {language_name} word itself
6. english_meaning: Direct synonym English meaning

Choose diverse topics and ensure the words are commonly used. Vary the difficulty levels.

Respond ONLY with valid JSON in this exact format:
{{
  "flashcards": [
    {{
      "syllables": "pronunciation-with-STRESS",
      "meaning": "brief translation",
      "topic_name": "Topic Name",
      "sub_topic_name": "Subtopic Name",
      "word": "word_in_{language_name}",
      "english_meaning": "Direct synonym English"
    }},
    ... (4 more items)
  ],
  "language": "{language}"
}}

Be accurate and educational."""

        user_message = f"Generate 5 {language_name} flashcards with diverse topics"

        response = self.gemini_client.models.generate_content(
            model="gemma-3-27b-it",
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

            flashcards = []
            for item in result.get("flashcards", []):
                flashcards.append(FlashcardItem(
                    syllables=item.get("syllables", ""),
                    meaning=item.get("meaning", ""),
                    topic_name=item.get("topic_name", ""),
                    sub_topic_name=item.get("sub_topic_name", ""),
                    word=item.get("word", ""),
                    english_meaning=item.get("english_meaning", "")
                ))

            return FlashcardResponse(flashcards=flashcards, language=language)

        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return FlashcardResponse(flashcards=[], language=language)

    def validate_flashcard(self, word: str, user_response: str) -> bool:
        """Validate if user's response matches the correct word.

        Args:
            word: The correct word
            user_response: The user's answer

        Returns:
            bool: True if the responses match (case-insensitive), False otherwise
        """
        # Normalize both strings: strip whitespace, convert to lowercase
        normalized_word = word.strip().lower()
        normalized_response = user_response.strip().lower()
        
        return normalized_word == normalized_response


# Initialize service
flashcards_service = FlashcardsService()
