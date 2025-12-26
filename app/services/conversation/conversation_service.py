"""Conversation practice service for language learners."""
import google.genai as genai
import random
import uuid
import re
from app.core.config import settings
from .conversation_schema import ConversationStartResponse, ConversationReplyResponse


class ConversationService:
    """Service for sequential conversation practice for language learners."""

    MAX_QUESTIONS = 5

    # Greeting phrases to start conversations
    GREETING_PHRASES = {
        "en-US": "How are you?",
        "tl-PH": "Kumusta ka?",
        "es-ES": "¿Cómo estás?",
        "fr-FR": "Comment ça va?",
        "de-DE": "Wie geht es dir?",
        "ja-JP": "Ogenki desu ka?",
        "zh-CN": "Nǐ hǎo ma?",
        "ko-KR": "Annyeonghaseyo?"
    }

    FALLBACK_QUESTIONS = {
        "en-US": [
            "What do you eat for breakfast?",
            "How do you go to work?",
            "What do you do on weekends?",
            "Do you like cooking?",
            "What is your favorite season?",
            "Do you exercise every day?",
            "What music do you like?",
            "Do you have any pets?",
            "What time do you wake up?",
            "What is your favorite food?",
            "Do you like reading books?",
            "What do you do for fun?",
            "Do you like outdoor activities?"
        ],
        "tl-PH": [
            "Ano ang kinakain mo sa almusal?",
            "Paano ka pumupunta sa trabaho?",
            "Ano ang ginagawa mo sa weekends?",
            "Gusto mo bang magluto?",
            "Ano ang paborito mong season?",
            "Nag-eehersisyo ka ba araw-araw?",
            "Anong musika ang gusto mo?",
            "May alagang hayop ka ba?",
            "Anong oras ka gumigising?",
            "Ano ang paborito mong pagkain?",
            "Gusto mo bang magbasa?",
            "Ano ang ginagawa mo para magsaya?",
            "Gusto mo ba ng outdoor activities?"
        ],
        "es-ES": [
            "¿Qué comes para el desayuno?",
            "¿Cómo vas al trabajo?",
            "¿Qué haces los fines de semana?",
            "¿Te gusta cocinar?",
            "¿Cuál es tu estación favorita?",
            "¿Haces ejercicio todos los días?",
            "¿Qué música te gusta?",
            "¿Tienes mascotas?",
            "¿A qué hora te despiertas?",
            "¿Cuál es tu comida favorita?",
            "¿Te gusta leer libros?",
            "¿Qué haces para divertirte?",
            "¿Te gustan las actividades al aire libre?"
        ]
    }

    def __init__(self):
        """Initialize the Gemini client."""
        self.gemini_client = genai.Client(api_key=settings.get_api_key())
        self.active_conversations = {}  # Store active conversation IDs temporarily with current phrase

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize text for consistent comparison."""
        return re.sub(r'[^\w\s]', '', text).lower().strip()

    def _get_fallback_questions(self, language: str):
        """Return fallback questions for the requested language."""
        return self.FALLBACK_QUESTIONS.get(language, self.FALLBACK_QUESTIONS["en-US"])

    
        

    async def start_conversation(self, language: str = "en-US") -> ConversationStartResponse:
        """Start a conversation practice session with a greeting.

        Args:
            language: Language code for the conversation

        Returns:
            ConversationStartResponse with the greeting phrase
        """
        # Only keep one active conversation at a time per product requirement
        self.active_conversations.clear()
        conversation_id = str(uuid.uuid4())

        # Get greeting phrase for the language
        target_phrase = self.GREETING_PHRASES.get(language, self.GREETING_PHRASES["en-US"])
        normalized_phrase = self._normalize_text(target_phrase)
        greeting_message = f"{target_phrase}"

        # Store the conversation ID as active
        self.active_conversations[conversation_id] = {
            "language": language,
            "current_phrase": target_phrase,  # Store the phrase user needs to repeat
            "question_count": 0,  # Track number of questions asked (max 5)
            "asked_questions": [normalized_phrase],  # Track asked questions to avoid repeats
            "created_at": uuid.uuid4()  # Using uuid for timestamp placeholder
        }

        return ConversationStartResponse(
            conversation_id=conversation_id,
            ai_message=greeting_message
        )

    async def reply_to_conversation(
        self, 
        conversation_id: str, 
        user_message: str, 
        language: str = "en-US"
    ) -> ConversationReplyResponse:
        """Generate a random daily life question for user to repeat.

        Args:
            conversation_id: The conversation ID (must be active)
            user_message: User's attempt to repeat the phrase
            language: Language code

        Returns:
            ConversationReplyResponse with random daily life question
        """
        # Check if conversation ID exists and is active
        if conversation_id not in self.active_conversations:
            return ConversationReplyResponse(
                ai_message="Conversation not found. Please start a new conversation.",
                conversation_ended=True
            )
        
        # Get the current phrase the user needs to repeat
        conv_data = self.active_conversations[conversation_id]
        current_phrase = conv_data.get("current_phrase", "")
        
        # Normalize both strings for comparison (remove punctuation, lowercase, strip)
        normalized_user_message = self._normalize_text(user_message)
        normalized_current_phrase = self._normalize_text(current_phrase)
        
        # Check if user's message matches the current phrase
        if normalized_user_message != normalized_current_phrase:
            return ConversationReplyResponse(
                ai_message=f"Please say {current_phrase} again.",
                conversation_ended=False
            )
        
        # Increment question count after correct answer
        conv_data["question_count"] += 1

       
        
        # Check if we've reached 5 questions
        if conv_data["question_count"] >= self.MAX_QUESTIONS:
            # Remove conversation from active list
            del self.active_conversations[conversation_id]
            return ConversationReplyResponse(
                ai_message=f"You've completed all {self.MAX_QUESTIONS} prompts. Fantastic work!",
                conversation_ended=True
            )
        
        # Pick random fallback question that hasn't been asked
        language_fallbacks = self._get_fallback_questions(language)
        asked_questions = conv_data.get("asked_questions", [])
        
        # Filter out already asked questions
        available_questions = [
            q for q in language_fallbacks
            if self._normalize_text(q) not in asked_questions
        ]
        
        # If all questions have been asked, just pick a random one
        if not available_questions:
            available_questions = language_fallbacks
        
        next_question = random.choice(available_questions)
        asked_questions.append(self._normalize_text(next_question))
        
        # Update the current phrase in the active conversation
        self.active_conversations[conversation_id]["current_phrase"] = next_question

        return ConversationReplyResponse(
            ai_message=f"{next_question}",
            conversation_ended=False
        )


# Initialize service
conversation_service = ConversationService()
