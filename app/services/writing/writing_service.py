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

    async def evaluate_response(self, prompt: str, user_response: str, language: str = "en-US") -> EvaluationResponse:
        """Evaluate a user's writing response.
        
        Args:
            prompt: The original writing prompt (in English)
            user_response: User's written response (in their chosen language)
            language: Language code of the response
            
        Returns:
            EvaluationResponse with rating and feedback
        """
        language_name = settings.supported_languages.get(language, "Tagalog")
        
        system_prompt = f"""You are a supportive language teacher evaluating {language_name} writing practice.

IMPORTANT: The prompt is in English, but the user's response is in {language_name}. Evaluate the {language_name} response based on how well it addresses the English prompt.

Task: Evaluate the user's response and provide:
1. A rating: "excellent", "good", or "need to improve"
2. Exactly 2-3 sentences of feedback on how good the response is. The 3 points are: 
    2.1 If the response is relavent to question.
    2.2 How good the grammar is.
    2.3 Suggestions for improvement(For excellent responses, write you're doing great).
3. Each feedback line MUST not exceed 10 words

Respond ONLY with valid JSON in this exact format:
{{
  "rating": "excellent|good|need to improve",
  "feedback": ["point 2.1", "point 2.2", "point 2.3"]
}}

Rating criteria:
- "excellent": Clear, well-structured, natural {language_name} language use, good grammar, addresses the prompt well
- "good": Understandable with minor issues, decent effort, somewhat addresses the prompt
- "need to improve": Confusing, major grammar issues, very short/incomplete, or doesn't address the prompt

Make feedback specific, encouraging, and actionable. Keep each point to 5-6 words. Provide feedback in English."""
        
        user_message = f"""Prompt (in English): {prompt}

User's Response (in {language_name}): {user_response}

Evaluate this {language_name} response."""
        
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
            rating = result.get("rating", "good")
            feedback = result.get("feedback", ["Response received.", "Keep practicing!", "Try more details."])
            
            # Ensure feedback is a list of exactly 3 strings
            if not isinstance(feedback, list) or len(feedback) != 3:
                feedback = ["Response received.", "Keep practicing!", "Try more details."]
            
            return EvaluationResponse(rating=rating, feedback=feedback)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return EvaluationResponse(
                rating="good",
                feedback=["Response received.", "Keep practicing!", "Try more details."]
            )



# Initialize service
writing_service = WritingService()
