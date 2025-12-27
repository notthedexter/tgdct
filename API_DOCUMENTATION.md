# Language Learning Platform - API Documentation

## Overview

The Language Learning Platform is a comprehensive FastAPI-based application that provides AI-powered language learning tools. It offers speech recognition, text-to-speech synthesis, writing practice, dictionary services, flashcards, roleplay scenarios, conversations, listening practice, stories, and dialogue generation.

**Base URL:** `http://127.0.0.1:8054`

**Version:** 2.0.0

---

## Table of Contents

1. [General Endpoints](#general-endpoints)
2. [Speech-to-Text (STT)](#speech-to-text-stt)
3. [Text-to-Speech (TTS)](#text-to-speech-tts)
4. [Writing Practice](#writing-practice)
5. [Dictionary](#dictionary)
6. [Flashcards](#flashcards)
7. [AI Roleplay](#ai-roleplay)
8. [Sequential Conversation Practice](#sequential-conversation-practice)
9. [Listening Practice](#listening-practice)
10. [AI Story](#ai-story)
11. [Dialogue Builder](#dialogue-builder)
12. [Supported Languages](#supported-languages)
13. [Error Handling](#error-handling)

---

## General Endpoints

### Get API Information

Returns basic information about the API and available endpoints.

**Endpoint:** `GET /`

**Response:**
```json
{
  "name": "Language Learning Platform",
  "description": "Speech-to-Text and Writing Practice using AI",
  "version": "2.0.0",
  "endpoints": {
    "languages": "/languages",
    "transcribe": "/transcribe",
    "writing": "/writing",
    "dictionary": "/dictionary",
    "flashcards": "/flashcards",
    "roleplay": "/roleplay"
  }
}
```

### Get Supported Languages

Returns a list of all supported languages.

**Endpoint:** `GET /languages`

**Response:**
```json
{
  "default_language": "en-US",
  "supported_languages": {
    "en-US": "English",
    "es-ES": "Spanish",
    "fr-FR": "French",
    "de-DE": "German",
    "it-IT": "Italian",
    "pt-BR": "Portuguese",
    "ja-JP": "Japanese",
    "ko-KR": "Korean",
    "zh-CN": "Mandarin Chinese",
    "ru-RU": "Russian",
    "ar-SA": "Arabic",
    "tl-PH": "Tagalog",
    "hi-IN": "Hindi",
    "th-TH": "Thai",
    "vi-VN": "Vietnamese",
    "nl-NL": "Dutch",
    "pl-PL": "Polish",
    "tr-TR": "Turkish",
    "sv-SE": "Swedish",
    "no-NO": "Norwegian"
  },
  "total_languages": 20
}
```

---

## Speech-to-Text (STT)

### Transcribe Audio

Converts speech from an audio file to text using Google's Gemini API.

**Endpoint:** `POST /transcribe`

**Request Type:** `multipart/form-data`

**Parameters:**
- `audio_file` (file, required): Audio file to transcribe (supports various formats)
- `language` (string, optional): Target language code (default: "en-US")

**Example Request (cURL):**
```bash
curl -X POST "http://127.0.0.1:8054/transcribe" \
  -F "audio_file=@recording.wav" \
  -F "language=en-US"
```

**Response:**
```json
{
  "transcribed_text": "Hello, how are you today?",
  "language": "en-US"
}
```

**Error Responses:**
- `400`: Unsupported language or empty audio file
- `500`: Internal server error during transcription

---

## Text-to-Speech (TTS)

### Synthesize Speech

Converts text to speech audio file.

**Endpoint:** `POST /synthesize`

**Request Type:** `application/json`

**Request Body:**
```json
{
  "text": "Hello, how are you?",
  "language": "en-US"
}
```

**Parameters:**
- `text` (string, required): Text to synthesize into speech
- `language` (string, required): Language code (currently supports "en-US" and "tl-PH")

**Example Request (cURL):**
```bash
curl -X POST "http://127.0.0.1:8054/synthesize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "language": "en-US"}' \
  --output speech.wav
```

**Response:**
Audio file (WAV format) with `Content-Type: audio/wav`

**Error Responses:**
- `400`: Unsupported language or empty text
- `500`: Internal server error during synthesis

---

## Writing Practice

### Generate Writing Prompt

Generates a creative writing prompt for language practice.

**Endpoint:** `POST /writing/generate-prompt`

**Parameters:**
- `language` (query, optional): Language code (default: "en-US")

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8054/writing/generate-prompt?language=es-ES"
```

**Response:**
```json
{
  "prompt": "Describe your favorite childhood memory",
  "language": "es-ES"
}
```

### Evaluate Writing Response

Evaluates user's written response and provides feedback.

**Endpoint:** `POST /writing/evaluate`

**Request Body:**
```json
{
  "prompt": "Describe your favorite childhood memory",
  "user_response": "Mi recuerdo favorito es cuando...",
  "language": "es-ES"
}
```

**Response:**
```json
{
  "feedback": "Great job! Your grammar is mostly correct...",
  "score": 8.5,
  "suggestions": ["Consider using past tense here..."],
  "corrected_text": "Mi recuerdo favorito fue cuando..."
}
```

---

## Dictionary

### Detect Object in Image

Detects objects in an image and returns the word with dictionary information.

**Endpoint:** `POST /dictionary/detect-image`

**Request Type:** `multipart/form-data`

**Parameters:**
- `image` (file, required): Image file containing the object
- `language` (string, optional): Target language code (default: "en-US")

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8054/dictionary/detect-image" \
  -F "image=@photo.jpg" \
  -F "language=tl-PH"
```

**Response:**
```json
{
  "word": "aso",
  "language": "tl-PH",
  "definition": "A domesticated carnivorous mammal...",
  "example_sentence": "Ang aso ay tumatahol sa gabi.",
  "pronunciation": "ah-so"
}
```

### Search Word

Searches for a word in the dictionary and returns its information.

**Endpoint:** `POST /dictionary/search`

**Parameters:**
- `word` (query, required): Word to search
- `language` (query, optional): Language code (default: "en-US")

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8054/dictionary/search?word=perro&language=es-ES"
```

**Response:**
```json
{
  "word": "perro",
  "language": "es-ES",
  "definition": "Animal doméstico de la familia de los cánidos...",
  "example_sentence": "El perro está en el jardín.",
  "pronunciation": "pe-rro",
  "synonyms": ["can", "chucho"]
}
```

---

## Flashcards

### Generate Flashcards

Generates 5 vocabulary flashcards for language learning.

**Endpoint:** `POST /flashcards/generate`

**Parameters:**
- `language` (query, optional): Language code (default: "en-US")

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8054/flashcards/generate?language=fr-FR"
```

**Response:**
```json
{
  "flashcards": [
    {
      "word": "maison",
      "translation": "house",
      "example": "J'habite dans une grande maison.",
      "pronunciation": "may-zon"
    },
    {
      "word": "livre",
      "translation": "book",
      "example": "Je lis un livre intéressant.",
      "pronunciation": "lee-vruh"
    }
    // ... 3 more flashcards
  ],
  "language": "fr-FR",
  "total_cards": 5
}
```

---

## AI Roleplay

### Generate Roleplay Scenario

Generates a random, diverse roleplay scenario with a question for language practice.

**Endpoint:** `POST /roleplay/generate-scenario`

**Parameters:**
- `language` (query, optional): Language code (default: "en-US")

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8054/roleplay/generate-scenario?language=de-DE"
```

**Response:**
```json
{
  "scenario": "You are at a grocery store. The cashier asks about your preferred payment method.",
  "question_in_language": "Wie möchten Sie bezahlen?",
  "question_english": "How would you like to pay?",
  "language": "de-DE"
}
```

**Scenario Categories:**
- Shopping (stores, markets, prices)
- Travel (airports, hotels, directions)
- Social (meeting friends, introductions)
- Dining (restaurants, ordering food)
- Healthcare (clinics, pharmacies)
- Work/School (colleagues, assignments)
- Public Services (banks, transportation)
- Entertainment (movies, museums)
- Home/Daily Life (neighbors, household tasks)

### Evaluate Roleplay Response

Evaluates user's response to a roleplay scenario and provides improvement suggestions.

**Endpoint:** `POST /roleplay/evaluate-response`

**Request Body:**
```json
{
  "scenario": "You are at a grocery store...",
  "question_in_language": "Wie möchten Sie bezahlen?",
  "question_english": "How would you like to pay?",
  "user_response": "Ich möchte mit Karte bezahlen.",
  "language": "de-DE"
}
```

**Response:**
```json
{
  "needs_improvement": false,
  "original": null,
  "better": null
}
```

Or if improvement is needed:
```json
{
  "needs_improvement": true,
  "original": "Ich will Karte bezahlen",
  "better": "Ich möchte mit Karte bezahlen"
}
```

---

## Sequential Conversation Practice

A conversation practice system where the AI provides phrases/questions/statements for the user to repeat. The conversation continues for 5 exchanges.

### Start Conversation

Starts a new conversation practice session with a greeting.

**Endpoint:** `POST /conversation/start`

**Parameters:**
- `language` (query, optional): Language code (default: "en-US")

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8054/conversation/start?language=tl-PH"
```

**Response:**
```json
{
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "ai_message": "Kumusta ka?"
}
```

### Reply to Conversation

Continues the conversation by checking if the user repeated the phrase correctly.

**Endpoint:** `POST /conversation/reply`

**Request Body:**
```json
{
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "user_message": "Kumusta ka",
  "language": "tl-PH"
}
```

**Response (Correct):**
```json
{
  "ai_message": "Ano ang kinakain mo sa almusal?",
  "conversation_ended": false
}
```

**Response (Incorrect):**
```json
{
  "ai_message": "Please say Kumusta ka? again.",
  "conversation_ended": false
}
```

**Response (Conversation Complete - after 5 prompts):**
```json
{
  "ai_message": "You've completed all 5 prompts. Fantastic work!",
  "conversation_ended": true
}
```

**Features:**
- AI randomly alternates between questions (60%) and general statements (40%)
- Tracks asked phrases to avoid repetition
- Normalizes text for comparison (removes punctuation, case-insensitive)
- Supports up to 5 phrase exchanges per conversation

---

## Listening Practice

### Generate Listening Practice

Generates 5 listening comprehension questions based on a topic.

**Endpoint:** `POST /listening/generate-practice`

**Request Body:**
```json
{
  "topic": "Daily routines",
  "language": "ja-JP"
}
```

**Response:**
```json
{
  "topic": "Daily routines",
  "language": "ja-JP",
  "questions": [
    {
      "audio_text": "毎朝七時に起きます",
      "question": "What time does the person wake up?",
      "options": ["6 AM", "7 AM", "8 AM", "9 AM"],
      "correct_answer": "7 AM"
    }
    // ... 4 more questions
  ],
  "total_questions": 5
}
```

---

## AI Story

### Generate Story

Generates a short story (7-8 lines maximum) based on a topic.

**Endpoint:** `POST /story/generate-story`

**Request Body:**
```json
{
  "topic": "A magical forest adventure",
  "language": "ko-KR"
}
```

**Response:**
```json
{
  "story": "옛날 옛적에 마법의 숲이 있었습니다...\n(7-8 lines of story)",
  "topic": "A magical forest adventure",
  "language": "ko-KR",
  "line_count": 8
}
```

---

## Dialogue Builder

### Generate Dialogue

Generates a grammar-focused dialogue based on a scenario.

**Endpoint:** `POST /dialogue/generate-dialogue`

**Request Body:**
```json
{
  "scenario": "Two friends meeting at a café",
  "language": "it-IT"
}
```

**Response:**
```json
{
  "dialogue": [
    {
      "speaker": "Person A",
      "text": "Ciao! Come stai?"
    },
    {
      "speaker": "Person B",
      "text": "Sto bene, grazie! E tu?"
    }
    // ... more dialogue lines
  ],
  "scenario": "Two friends meeting at a café",
  "language": "it-IT",
  "grammar_focus": "Present tense greetings and polite expressions"
}
```

---

## Supported Languages

The API supports 20 languages for various learning activities:

| Code | Language |
|------|----------|
| en-US | English |
| es-ES | Spanish |
| fr-FR | French |
| de-DE | German |
| it-IT | Italian |
| pt-BR | Portuguese |
| ja-JP | Japanese |
| ko-KR | Korean |
| zh-CN | Mandarin Chinese |
| ru-RU | Russian |
| ar-SA | Arabic |
| tl-PH | Tagalog |
| hi-IN | Hindi |
| th-TH | Thai |
| vi-VN | Vietnamese |
| nl-NL | Dutch |
| pl-PL | Polish |
| tr-TR | Turkish |
| sv-SE | Swedish |
| no-NO | Norwegian |

**Note:** Some features may have limited language support. Check individual endpoint documentation for specific language availability.

---

## Error Handling

All endpoints follow a consistent error response format:

### Common HTTP Status Codes

- `200`: Success
- `400`: Bad Request (invalid parameters, unsupported language, etc.)
- `404`: Not Found (conversation not found, etc.)
- `500`: Internal Server Error

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Scenarios

1. **Unsupported Language:**
```json
{
  "detail": "Unsupported language. Supported: en-US, es-ES, fr-FR, ..."
}
```

2. **Empty Input:**
```json
{
  "detail": "Text cannot be empty"
}
```

3. **Conversation Not Found:**
```json
{
  "detail": "Conversation not found. Please start a new conversation."
}
```

4. **Invalid File:**
```json
{
  "detail": "Empty audio file"
}
```

---

## CORS Configuration

The API allows cross-origin requests from all origins (`*`). In production, this should be restricted to specific domains.

```python
allow_origins=["*"]
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

---

## Running the API

### Prerequisites

- Python 3.8+
- Required environment variables:
  - `GEMINI_API_KEY`: Google Gemini API key
  - `GROQ_API_KEY`: Groq API key (for some features)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Start the Server

```bash
# Development mode with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --host 127.0.0.1 --port 8054 --reload
```

### Using Docker

```bash
# Build the image
docker build -t language-learning-platform .

# Run the container
docker run -p 8054:8054 --env-file .env language-learning-platform
```

### Using Docker Compose

```bash
docker-compose up
```

---

## API Testing

### Interactive Documentation

Once the server is running, visit:

- **Swagger UI:** `http://127.0.0.1:8054/docs`
- **ReDoc:** `http://127.0.0.1:8054/redoc`

These provide interactive API documentation where you can test endpoints directly in your browser.

### Example Test Workflow

1. **Check supported languages:**
   ```bash
   curl http://127.0.0.1:8054/languages
   ```

2. **Start a conversation:**
   ```bash
   curl -X POST "http://127.0.0.1:8054/conversation/start?language=tl-PH"
   ```

3. **Generate flashcards:**
   ```bash
   curl -X POST "http://127.0.0.1:8054/flashcards/generate?language=es-ES"
   ```

4. **Generate roleplay scenario:**
   ```bash
   curl -X POST "http://127.0.0.1:8054/roleplay/generate-scenario?language=fr-FR"
   ```

---

## Rate Limiting and Best Practices

1. **API Key Management:** Store API keys securely in environment variables
2. **File Size Limits:** Audio files should be reasonably sized (recommended < 10MB)
3. **Request Frequency:** Be mindful of API rate limits from third-party services (Gemini, Groq)
4. **Language Support:** Always check language support before making requests
5. **Error Handling:** Implement proper error handling in client applications

---

## Support and Contributing

For issues, questions, or contributions, please contact the development team.

**Project Repository:** [Add your repository URL here]

**Version:** 2.0.0  
**Last Updated:** December 27, 2025
