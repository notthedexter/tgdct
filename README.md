# Language Learning Platform

A comprehensive FastAPI-based language learning platform with **multi-language support**. Practice any of 20+ languages with AI-powered features including speech-to-text, writing practice, dictionary lookup, flashcards, and roleplay scenarios.

## 🌍 Supported Languages

The platform supports **20+ languages** including:
- **English** (en-US) - Default
- **Spanish** (es-ES)
- **French** (fr-FR)
- **German** (de-DE)
- **Italian** (it-IT)
- **Portuguese** (pt-BR)
- **Japanese** (ja-JP)
- **Korean** (ko-KR)
- **Mandarin Chinese** (zh-CN)
- **Russian** (ru-RU)
- **Arabic** (ar-SA)
- **Hindi** (hi-IN)
- **Thai** (th-TH)
- **Vietnamese** (vi-VN)
- **Dutch** (nl-NL)
- **Polish** (pl-PL)
- **Turkish** (tr-TR)
- **Swedish** (sv-SE)
- **Norwegian** (no-NO)
- **Tagalog** (tl-PH)

Get the full list at: `GET /languages`

## Project Structure

```
cp_duol/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Application configuration
│   ├── services/
│   │   ├── __init__.py
│   │   └── stt/                   # Speech-to-Text service
│   │       ├── __init__.py
│   │       ├── stt_route.py       # API routes
│   │       └── stt_schema.py      # Pydantic schemas
│   └── utils/                     # Reusable utilities
├── main.py                        # FastAPI application entry point
├── requirements.txt
└── README.md
```

## Features

- � **Multi-language Support** - Learn from 20+ languages
- 🎤 **Speech-to-Text** - Transcribe audio in any supported language
- ✍️ **Writing Practice** - Get AI-generated prompts and detailed feedback
- 📚 **Dictionary** - Look up words with pronunciations, meanings, and examples
- 🃏 **Flashcards** - Generate vocabulary flashcards for any language
- 🎭 **AI Roleplay** - Practice conversations with context-aware scenarios
- 🆓 **Free to use** - Powered by Google Gemini and Groq APIs
- ⚡ **Fast and efficient** - Real-time responses
- 🏗️ **Clean architecture** - Modular microservices design

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd tagalog_dict
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys:
# GEMINI_API_KEY=your_key_here
# GROQ_API_KEY=your_key_here
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Usage

### Running Locally

```bash
python main.py
```

The API will be available at `http://localhost:8054`

### Running with Docker

```bash
# Build and run
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# Stop services
docker-compose down
```

### API Documentation

Once running, visit:
- **Interactive API docs**: `http://localhost:8054/docs`
- **ReDoc**: `http://localhost:8054/redoc`

## API Examples

### 1. Get Supported Languages
```bash
curl http://localhost:8054/languages
```

### 2. Speech-to-Text (Transcription)
```bash
curl -X POST "http://localhost:8054/transcribe?language=es-ES" \
  -F "audio_file=@audio.wav"
```

### 3. Generate Writing Prompt
```bash
curl -X POST "http://localhost:8054/writing/generate-prompt?language=fr-FR"
```

### 4. Evaluate Writing
```bash
curl -X POST "http://localhost:8054/writing/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write about your family",
    "user_response": "Ma famille est grande...",
    "language": "fr-FR"
  }'
```

### 5. Dictionary Search
```bash
curl -X POST "http://localhost:8054/dictionary/search?word=casa&language=es-ES"
```

### 6. Generate Flashcards
```bash
curl -X POST "http://localhost:8054/flashcards/generate?language=ja-JP"
```

### 7. Generate Roleplay Scenario
```bash
curl -X POST "http://localhost:8054/roleplay/generate-scenario?language=ko-KR"
```

### 8. Evaluate Roleplay Response
```bash
curl -X POST "http://localhost:8054/roleplay/evaluate-response" \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "You are at a restaurant",
    "question_in_language": "무엇을 드시겠어요?",
    "question_english": "What would you like to eat?",
    "user_response": "비빔밥 주세요",
    "language": "ko-KR"
  }'
```

## Environment Variables

Required environment variables (add to `.env` file):

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```
- 🎙️ **Real-time Speech Recognition**: Click "Start Speaking" and the browser will transcribe as you speak
- 🌍 **Choose Language**: Select Tagalog (default) or English before starting
- ✨ **Live Transcription**: See your words appear in real-time as you speak

**Browser Support:**
- ✅ Google Chrome
- ✅ Microsoft Edge
- ✅ Safari
- ❌ Firefox (limited support)

## API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## Supported Languages

- **English (en-US)** - Default
- **English US (en-US)**
- **English UK (en-GB)**

## How It Works

This application uses the **Web Speech API** which is built into modern browsers. The speech recognition happens entirely in the browser using Google's speech recognition service, which is free and requires no API key. The browser streams audio to Google's servers and returns the transcribed text in real-time.
