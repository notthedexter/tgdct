"""Listening practice service using Gemini API for generating questions."""
import google.genai as genai
from app.core.config import settings
from .listening_schema import ListeningRequest, ListeningResponse, ListeningQuestion, ListeningOption, ListeningAnswerEvaluation
import json


class ListeningPracticeService:
    """Service for generating listening practice questions with multiple choice answers."""

    def __init__(self):
        """Initialize the Gemini client."""
        self.gemini_client = genai.Client(api_key=settings.get_api_key())

    async def generate_listening_practice(self, topic: str, language: str = "tl-PH") -> ListeningResponse:
        """Generate 5 listening practice questions based on the topic.

        Args:
            topic: The topic for the listening practice
            language: Language code (default: tl-PH for Tagalog)

        Returns:
            ListeningResponse with 5 questions, each having 4 options (one correct)
        """
        language_name = settings.supported_languages.get(language, "Tagalog")

        json_format = """
JSON Format:
{
  "topic": "brief description of the listening practice topic",
  "questions": [
    {
      "question": "Question about the topic in the target language",
      "options": [
        {"text": "Option 1"},
        {"text": "Option 2"},
        {"text": "Option 3"},
        {"text": "Option 4"}
      ],
      "correct_option_index": 0-3
    }
  ]
}"""

        system_prompt = f"""You are a listening practice builder for {language_name} language learning.

OBJECTIVE:
Generate exactly 5 listening comprehension questions based on the given topic. Each question should have exactly 4 multiple choice options in {language_name}, where only one answer is correct.

Instructions:
1. Generate exactly 5 questions about the topic.
2. Questions should test listening comprehension and understanding.
3. Each question must have exactly 4 options.
4. Only one option should be correct.
5. The incorrect options should be plausible but clearly wrong.
6. Questions should be appropriate for language learners.
7. Vary the difficulty from easy to moderate.
8. IMPORTANT: Questions must be in Tagalog ({language_name}), but ALL answer options must be in English.
9. Output ONLY valid JSON in the specified format.

Example question types:
- Comprehension questions about a passage
- Questions about specific details
- Questions about main ideas
- Questions about context or meaning
- Questions about vocabulary in context

""" + json_format

        user_message = f"Generate 5 listening practice questions for this topic: {topic}"

        response = self.gemini_client.models.generate_content(
            model="gemma-3-27b-it",
            contents=f"{system_prompt}\n\n{user_message}",
            config={
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40
            }
        )

        response_text = response.text.strip()

        # Parse JSON response
        try:
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            data = json.loads(response_text)

            # Validate we have exactly 5 questions
            if len(data.get("questions", [])) != 5:
                raise ValueError("Expected exactly 5 questions")

            # Validate each question has exactly 4 options
            for q in data["questions"]:
                if len(q.get("options", [])) != 4:
                    raise ValueError("Each question must have exactly 4 options")

            # Convert to Pydantic models
            questions = [
                ListeningQuestion(
                    question=q["question"],
                    options=[ListeningOption(text=opt["text"]) for opt in q["options"]],
                    correct_option_index=q["correct_option_index"]
                )
                for q in data["questions"]
            ]

            return ListeningResponse(
                topic=data["topic"],
                questions=questions
            )

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")
        except KeyError as e:
            raise ValueError(f"Missing required field in response: {e}")

    def evaluate_answer(self, question: ListeningQuestion, selected_option_index: int) -> ListeningAnswerEvaluation:
        """Evaluate if the selected answer is correct.

        Args:
            question: The question being answered
            selected_option_index: Index of the option selected by the user

        Returns:
            ListeningAnswerEvaluation with result and explanation
        """
        is_correct = selected_option_index == question.correct_option_index
        correct_answer = question.options[question.correct_option_index].text

        if is_correct:
            explanation = "Correct! Well done."
        else:
            selected_answer = question.options[selected_option_index].text
            explanation = f"Incorrect. You selected '{selected_answer}', but the correct answer is '{correct_answer}'."

        return ListeningAnswerEvaluation(
            is_correct=is_correct,
            correct_answer=correct_answer,
            explanation=explanation
        )


# Create singleton instance
listening_practice_service = ListeningPracticeService()
