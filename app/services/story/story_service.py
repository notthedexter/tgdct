"""AI story service using Gemini API for generating short stories."""
import google.genai as genai
from app.core.config import settings
from .story_schema import StoryRequest, StoryResponse


class AIStoryService:
    """Service for generating short stories using Gemini API."""

    def __init__(self):
        """Initialize the Gemini client."""
        self.gemini_client = genai.Client(api_key=settings.get_api_key())

    async def generate_story(self, topic: str, language: str = "tl-PH") -> StoryResponse:
        """Generate a short story (7-8 lines maximum) based on the topic.

        Args:
            topic: The topic for the story
            language: Language code (default: tl-PH for Tagalog)

        Returns:
            StoryResponse with the generated story
        """
        language_name = settings.supported_languages.get(language, "Tagalog")

        system_prompt = f"""You are a creative storyteller for {language_name} language learning.

OBJECTIVE:
Generate a short, engaging story based on the given topic. The story must be 7-8 lines maximum, written as continuous text without line breaks.

Instructions:
1. Write the story in {language_name} as ONE CONTINUOUS PARAGRAPH.
2. Keep the story to 7-8 lines maximum when formatted, but write it as continuous text.
3. Make it engaging and appropriate for language learners.
4. Include a clear beginning, middle, and end.
5. Use simple vocabulary and sentence structures.
6. Focus on storytelling elements: characters, setting, plot, and conclusion.
7. DO NOT use line breaks (\n) or separate the story into lines.
8. Dont include any sorts of special stuff like ** or --- or \n or anything like that.
9. Output ONLY the story text, no additional formatting or explanations.

Story Structure Guidelines:
- Start with introduction/setting and main character
- Continue with main events/plot development
- Include climax and resolution
- End with conclusion

Keep it concise but complete! Write as one flowing paragraph."""

        user_message = f"Generate a 7-8 line story (as continuous text) about: {topic}"

        response = self.gemini_client.models.generate_content(
            model="gemma-3-27b-it",
            contents=f"{system_prompt}\n\n{user_message}",
            config={
                "temperature": 0.8,
                "top_p": 0.9,
                "top_k": 50
            }
        )

        story_target = response.text.strip()

        # Remove any line breaks and clean up
        story_target = story_target.replace('\n', ' ').replace('\r', ' ')
        # Clean up multiple spaces
        while '  ' in story_target:
            story_target = story_target.replace('  ', ' ')

        # Generate English version with same content
        english_prompt = f"""You are a translator. Translate this {language_name} story to English, keeping the same meaning and structure:

{story_target}

Instructions:
1. Translate accurately while maintaining the story's meaning
2. Keep it as ONE CONTINUOUS PARAGRAPH without line breaks
3. Use simple English appropriate for language learners
4. Dont include any sorts of special stuff like ** or --- or \n or anything like that.
5. Output ONLY the English translation, no additional text"""

        english_response = self.gemini_client.models.generate_content(
            model="gemma-3-27b-it",
            contents=english_prompt,
            config={
                "temperature": 0.3,  # Lower temperature for more accurate translation
                "top_p": 0.8,
                "top_k": 40
            }
        )

        story_english = english_response.text.strip()
        # Clean up any line breaks in English version too
        story_english = story_english.replace('\n', ' ').replace('\r', ' ')
        while '  ' in story_english:
            story_english = story_english.replace('  ', ' ')

        # Ensure stories are not too long (rough estimate: 7-8 lines = ~500 characters each)
        if len(story_target) > 800:
            story_target = story_target[:800] + "..."
        if len(story_english) > 800:
            story_english = story_english[:800] + "..."

        return StoryResponse(
            topic=topic,
            story_target_language=story_target,
            story_english=story_english,
            language=language
        )


# Create singleton instance
ai_story_service = AIStoryService()