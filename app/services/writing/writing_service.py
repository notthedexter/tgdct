"""Writing service using Gemini API for generating prompts and evaluating responses."""
import google.genai as genai
from app.core.config import settings
from .writing_schema import PromptResponse, EvaluationResponse
import json
import random


class WritingService:
    """Service for generating writing prompts and evaluating user responses."""

    # List of basic language learner question topics for short responses
    QUESTION_TOPICS = [
        "Favorite animals (cats, dogs, birds, etc.)",
        "Favorite foods and drinks",
        "Daily routines (what you do every day)",
        "Family members and relationships",
        "Hobbies and free time activities",
        "Weather and seasons",
        "Colors and favorite colors",
        "Numbers and counting",
        "Days of the week and months",
        "Clothing and what you wear",
        "Home and rooms in the house",
        "Transportation (car, bus, bike, etc.)",
        "Sports and games you like",
        "Music and favorite songs",
        "Movies and TV shows",
        "Friends and social activities",
        "School or work activities",
        "Travel and places you've visited",
        "Shopping and favorite stores",
        "Health and feeling well/sick",
        "Emotions and how you feel",
        "Time and telling time",
        "Money and shopping",
        "Nature and outdoor activities",
        "Technology and gadgets",
        "Dreams and future plans",
        "Pets and animals you know",
        "Food preparation and cooking",
        "Birthdays and celebrations",
        "Vacations and holidays"
    ]

    def __init__(self):
        """Initialize the Gemini client."""
        self.gemini_client = genai.Client(api_key=settings.get_api_key())

    async def generate_prompt(self, language: str = "en-US") -> PromptResponse:
        """Generate a writing prompt for the specified language using Gemini based on language learning topics.

        Args:
            language: Language code for prompt generation (e.g., en-US, es-ES, tl-PH)

        Returns:
            PromptResponse with a generated writing prompt (question only)
        """
        language_name = settings.supported_languages.get(language, "the target language")

        # Select a random topic from the predefined list
        selected_topic = random.choice(self.QUESTION_TOPICS)

        system_prompt = f"""You are a language learning question generator for {language_name}.

OBJECTIVE:
Generate ONE simple writing prompt/question based on the topic: {selected_topic}

Instructions:
1. Create a basic, everyday question that can be answered in 2-3 sentences.
2. Focus on personal opinions, preferences, or simple descriptions.
3. Examples: "What is your favorite animal and why?", "Do you like to go out with friends?"
4. Make it grammatically correct in {language_name}.
5. OUTPUT: Return ONLY the question/prompt string. No other text.
6. Keep it very simple and conversational.

"""

        user_message = f"Generate a writing prompt about: {selected_topic}"

        response = self.gemini_client.models.generate_content(
            model="gemma-3-27b-it",
            contents=f"{system_prompt}\n\n{user_message}",
            config={
                "temperature": 0.7,  
                "top_p": 0.8,        
                "top_k": 40         
            }
        )

        prompt = response.text.strip()

        # Ensure only one question, no details
        if "?" in prompt:
            prompt = prompt.split("?")[0] + "?"
        else:
            prompt = prompt.split(".")[0] + "."

        return PromptResponse(prompt=prompt)

    async def evaluate_response(
        self, 
        prompt: str, 
        user_response: str, 
        language: str = "en-US"
    ) -> EvaluationResponse:
        """Evaluate user's writing response using Gemini API.

        Args:
            prompt: The writing prompt that was given
            user_response: The user's written response
            language: Language code for evaluation context

        Returns:
            EvaluationResponse with rating, need_to_improve flag, feedback, and sample response
        """
        language_name = settings.supported_languages.get(language, "the target language")
        
        system_prompt = f"""You are a basic {language_name} language teacher evaluating beginner learners.

Your task is to evaluate student writing based ONLY on grammar accuracy:
- Check for basic grammar errors (verb tenses, subject-verb agreement, articles, prepositions)
- Ignore vocabulary, style, content, or advanced structures
- Focus on simple, clear sentences

Provide constructive feedback focused on grammar corrections only."""

        user_message = f"""Please evaluate the following {language_name} writing response to a prompt.

Prompt: {prompt}

Student's Response:
{user_response}

Evaluate ONLY for grammar accuracy. Provide your evaluation in JSON format with:
1. rating: "excellent" (no grammar errors), "good" (1-2 minor errors), or "need to improve" (multiple grammar errors)
2. need_to_improve: false if rating is "excellent", true otherwise
3. sample_response: A corrected version of the student's response with proper grammar

Respond ONLY with valid JSON in this exact format:
{{
  "rating": "excellent|good|need to improve",
  "need_to_improve": false,
  "sample_response": "Corrected version of the student's response"
}}"""

        try:
            message = self.gemini_client.models.generate_content(
                model="gemma-3-27b-it",
                contents=f"{system_prompt}\n\n{user_message}"
            )

            response_text = message.text.strip()

            # Parse JSON response
            try:
                # Remove markdown code blocks if present
                if response_text.startswith("```"):
                    response_text = response_text.split("```")[1]
                    if response_text.startswith("json"):
                        response_text = response_text[4:]
                    response_text = response_text.strip()

                result = json.loads(response_text)

                # Validate rating
                rating = result.get("rating", "need to improve").lower()
                if rating not in ["excellent", "good", "need to improve"]:
                    rating = "need to improve"

                # Set need_to_improve based on rating
                need_to_improve = rating != "excellent"

                sample_response = result.get("sample_response", "Unable to generate sample response.")

                return EvaluationResponse(
                    rating=rating,
                    need_to_improve=need_to_improve,
                    sample_response=sample_response
                )

            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return EvaluationResponse(
                    rating="need to improve",
                    need_to_improve=True,
                    sample_response="Unable to generate sample response."
                )

        except Exception as e:
            # Fallback for API errors
            return EvaluationResponse(
                rating="need to improve",
                need_to_improve=True,
                sample_response="Unable to generate sample response."
            )


# Initialize service
writing_service = WritingService()
