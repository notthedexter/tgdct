"""Dialogue builder service using Gemini API for generating conversational dialogues."""
import google.genai as genai
from app.core.config import settings
from .dialogue_schema import DialogueRequest, DialogueResponse, DialogueQuestion, DialogueOption, AnswerEvaluation
import json


class DialogueBuilderService:
    """Service for generating conversational dialogues with multiple choice questions."""

    def __init__(self):
        """Initialize the Gemini client."""
        self.gemini_client = genai.Client(api_key=settings.get_api_key())

    async def generate_dialogue(self, scenario: str, language: str = "en-US") -> DialogueResponse:
        """Generate a conversational dialogue with max 3 questions based on the scenario.

        Args:
            scenario: The scenario or prompt for the dialogue

        Returns:
            DialogueResponse with questions, each having 2 options (one correct)
        """
        language_name = settings.supported_languages.get(language, "the target language")

        json_format = """
JSON Format:
{
  "scenario": "brief description of the dialogue scenario",
  "questions": [
    {
      "question": "AI's statement or question in target language",
      "question_english": "AI's statement or question in English",
      "options": [
        {"text": "Wrong response in target language", "english_text": "Wrong response in English"},
        {"text": "Correct response in target language", "english_text": "Correct response in English"}
      ],
      "correct_option_index": 0 or 1
    }
  ]
}"""

        system_prompt = f"""You are a dialogue builder for {language_name} language learning.

OBJECTIVE:
Generate a conversational dialogue with a maximum of 3 questions. Each question shows what the AI says in BOTH {language_name} AND English, then provides exactly 2 response options for the user in BOTH languages, where only one response is appropriate/correct.

Instructions:
1. The dialogue should be based on the given scenario and build conversationally.
2. Each question should follow the flow of conversation.
3. For EVERY question, provide:
   - "question": The AI's statement/question in {language_name}
   - "question_english": The exact same statement/question in English
4. For EVERY option, provide:
   - "text": The response option in {language_name}
   - "english_text": The exact same response option in English
5. Provide exactly 2 response options: one appropriate/correct response, one inappropriate/wrong response.
6. The wrong response should be clearly incorrect for the context (like responding "Good night" to "Good morning").
7. Focus on conversational appropriateness, not just grammar.
8. Keep questions and options simple and appropriate for language learners.
9. Output ONLY valid JSON in the specified format.

Examples:
- AI (in {language_name}): "Good morning!" / (in English): "Good morning!"
  Options: 
    [{language_name}: "Good night!", English: "Good night!"], 
    [{language_name}: "Good morning!", English: "Good morning!"] (correct: second)

""" + json_format

        user_message = f"Generate a dialogue for this scenario: {scenario}"

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
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            result = json.loads(response_text)

            # Validate and convert to our models
            questions = []
            for q in result.get("questions", []):
                options = [
                    DialogueOption(
                        text=opt["text"],
                        english_text=opt.get("english_text", opt["text"])
                    ) for opt in q["options"]
                ]
                question = DialogueQuestion(
                    question=q["question"],
                    question_english=q.get("question_english", q["question"]),
                    options=options,
                    correct_option_index=q["correct_option_index"]
                )
                questions.append(question)

            return DialogueResponse(
                scenario=result.get("scenario", scenario),
                questions=questions[:3]  # Ensure max 3 questions
            )

        except (json.JSONDecodeError, KeyError) as e:
            # Fallback if parsing fails
            return DialogueResponse(
                scenario=scenario,
                questions=[]
            )

    def evaluate_answer(self, question: DialogueQuestion, selected_option_index: int) -> AnswerEvaluation:
        """Evaluate if the selected answer is correct.

        Args:
            question: The dialogue question
            selected_option_index: The index of the selected option

        Returns:
            AnswerEvaluation with correctness and explanation
        """
        is_correct = selected_option_index == question.correct_option_index
        correct_answer = question.options[question.correct_option_index].text

        if is_correct:
            explanation = "Correct! Well done."
        else:
            explanation = f"Incorrect. The correct answer is: {correct_answer}"

        return AnswerEvaluation(
            is_correct=is_correct,
            correct_answer=correct_answer,
            explanation=explanation
        )


# Initialize service
dialogue_builder_service = DialogueBuilderService()