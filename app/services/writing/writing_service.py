"""Writing practice service using Gemini API."""
import google.genai as genai
from app.core.config import settings
from .writing_schema import PromptResponse, EvaluationResponse
import json


class WritingService:
    """Service for generating writing prompts and evaluating responses."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        self.gemini_client = genai.Client(api_key=settings.get_api_key())
    
    def generate_prompt(self, language: str = "en-US") -> PromptResponse:
        """Generate a random writing prompt in English for language practice.
        
        Args:
            language: Language code for response context (not used for prompt generation)
            
        Returns:
            PromptResponse with the generated prompt in English
        """
        system_prompt = """You are a language teacher creating writing prompts in ENGLISH for language learners.
Generate ONE simple, engaging one-liner question IN ENGLISH that a beginner or intermediate learner can write about in their target language.
Examples: "Write about your family", "Describe your favorite food", "What did you do yesterday?", "Tell me about your hobbies"
Return ONLY the prompt text in English, nothing else."""
        
        response = self.gemini_client.models.generate_content(
            model="gemma-3-27b-it",
            contents=f"{system_prompt}\n\nGenerate a writing prompt in English"
        )
        
        prompt = response.text.strip()
        return PromptResponse(prompt=prompt)
    
    def evaluate_response(self, prompt: str, user_response: str, language: str = "en-US") -> EvaluationResponse:
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
            feedback = result.get("feedback", ["Keep practicing!"])
            
            return EvaluationResponse(rating=rating, feedback=feedback)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return EvaluationResponse(
                rating="good",
                feedback=["Response received. Keep practicing!", "Try to write more detailed responses."]
            )


# Initialize service
writing_service = WritingService()
