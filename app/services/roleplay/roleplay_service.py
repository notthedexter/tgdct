"""AI Roleplay service using Gemini API."""
import json
import random

import google.genai as genai
from google.genai import types

from app.core.config import settings
from .roleplay_schema import RoleplayScenarioResponse, RoleplayResponseEvaluation


class RoleplayService:
    """Service for AI-powered roleplay scenarios and response evaluation."""

    SCENARIO_CATEGORIES = [
        {
            "name": "Shopping",
            "focus": "Stores, markets, prices, availability, sizes, quantities."
        },
        {
            "name": "Travel",
            "focus": "Airports, stations, hotels, itineraries, directions, tickets."
        },
        {
            "name": "Social",
            "focus": "Meeting friends, making plans, introductions, casual chats."
        },
        {
            "name": "Dining",
            "focus": "Restaurants, cafes, ordering food, reservations, paying bills."
        },
        {
            "name": "Healthcare",
            "focus": "Clinics, pharmacies, symptoms, appointments, advice."
        },
        {
            "name": "Work or School",
            "focus": "Colleagues, teachers, assignments, schedules, requests."
        },
        {
            "name": "Public Services",
            "focus": "Government offices, banks, transportation services, utilities."
        },
        {
            "name": "Entertainment",
            "focus": "Movies, concerts, museums, sports, leisure plans."
        },
        {
            "name": "Home and Daily Life",
            "focus": "Neighbors, household tasks, repairs, deliveries, family."
        },
    ]

    def __init__(self):
        """Initialize the Gemini client."""
        self.gemini_client = genai.Client(api_key=settings.get_api_key())

    def generate_scenario(self, language: str = "en-US") -> RoleplayScenarioResponse:
        """Generate a simple roleplay scenario and question in the specified language.

        Args:
            language: Language code for the scenario question (e.g., tl-PH, es-ES, fr-FR)

        Returns:
            RoleplayScenarioResponse with scenario and questions
        """
        language_name = settings.supported_languages.get(language, "the target language")
        scenario_category = random.choice(self.SCENARIO_CATEGORIES)

        prompt = f"""Generate a vivid, everyday roleplay scenario for {language_name} learners.

Scenario category: {scenario_category['name']}
Category focus: {scenario_category['focus']}

Guidelines:
- Keep scenarios grounded in real life and culturally neutral unless specified.
- Vary names, locations, and details; do not reuse earlier ideas.
- Avoid defaulting to coffee shops or repeating the same institution type.
- The learner is directly involved and must answer the question you create.
- Create one clear, contextually relevant question in {language_name} that someone would ask in this scenario.
- Make sure the question is easy, simple and appropriate for language learners.

Respond with valid JSON in this exact format:
{{
    "scenario": "English description of a simple everyday scenario (2 sentences)",
    "question_in_language": "One simple question in {language_name} that someone would ask in this scenario in a language learning context",
    "question_english": "English translation of the same question",
    "language": "{language}"
}}

Ensure the question matches the selected scenario category and feels conversational."""

        response = self.gemini_client.models.generate_content(
            model="gemma-3-27b-it",
            contents=prompt
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
            return RoleplayScenarioResponse(
                scenario=result.get("scenario", ""),
                question_in_language=result.get("question_in_language", ""),
                question_english=result.get("question_english", ""),
                language=language
            )
        except json.JSONDecodeError:
            # Fallback
            return RoleplayScenarioResponse(
                scenario="You are meeting a friend. They ask how you are doing.",
                question_in_language="",
                question_english="How are you?",
                language=language
            )

    def evaluate_response(self, scenario: str, question_in_language: str,
                         question_english: str, user_response: str, language: str = "en-US") -> RoleplayResponseEvaluation:
        """Evaluate user's response and provide improvement if needed.

        Args:
            scenario: The scenario description
            question_in_language: The question in the target language
            question_english: The question in English
            user_response: User's response in the target language
            language: Language code of the response

        Returns:
            RoleplayResponseEvaluation with improvement suggestions
        """
        language_name = settings.supported_languages.get(language, "the target language")
        
        prompt = f"""Evaluate this {language_name} language learner's response in a roleplay scenario.

Scenario: {scenario}
Question ({language_name}): {question_in_language}
Question (English): {question_english}
Learner's Response: {user_response}

Analyze if the response is appropriate, natural, and grammatically correct for the context. Consider:
- Is it relevant to the question?
- Is the grammar correct?
- Is it natural {language_name} conversation?
- Is the politeness level appropriate?

If the response needs improvement, provide a better version in {language_name}.

Respond with valid JSON in this exact format:
{{{{
  "needs_improvement": true/false,
  "original": "the original response if improvement needed, otherwise null",
  "better": "improved version in {language_name} if needed, otherwise null"
}}}}

Only suggest improvement if there are clear issues with grammar, relevance, or naturalness."""

        response = self.gemini_client.models.generate_content(
            model="gemma-3-27b-it",
            contents=prompt
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
            return RoleplayResponseEvaluation(
                needs_improvement=result.get("needs_improvement", False),
                original=result.get("original"),
                better=result.get("better")
            )
        except json.JSONDecodeError:
            # Fallback - assume no improvement needed
            return RoleplayResponseEvaluation(
                needs_improvement=False,
                original=None,
                better=None
            )


# Initialize service
roleplay_service = RoleplayService()