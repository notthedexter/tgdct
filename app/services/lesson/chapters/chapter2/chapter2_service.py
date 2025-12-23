"""Chapter 2 Service - Action, Time and Place (A1 → A2)"""
import json
from difflib import get_close_matches
import google.genai as genai
from app.core.config import settings
from app.services.lesson.chapters.chapter2.chapter2_schema import (
    Chapter2GenerationRequest,
    Chapter2Response,
    Chapter2Content,
    ModuleContent,
    MODULE_NAMES,
    ModuleTitlesRequest,
    ModuleTitlesResponse
)


class Chapter2Service:
    """Service for generating complete Chapter 2 with all 7 modules"""

    def __init__(self):
        """Initialize the Gemini client"""
        self.gemini_client = genai.Client(api_key=settings.get_api_key())

    async def get_module_titles(self, request: ModuleTitlesRequest) -> ModuleTitlesResponse:
        """Get all module titles translated to target language"""
        try:
            language_code = request.target_language
            
            prompt = f"""Translate the following 7 module titles into {language_code}.

Module titles in English:
1. Places and Locations
2. Basic Feelings
3. Expressing Affection (Advanced Edition)
4. Expressing Surprises and Reactions
5. Time and Telling Time
6. Months of the Year
7. Days of the Week

Respond with ONLY a JSON object mapping module numbers to translated titles:
{{
  "1": "[Translation of Places and Locations]",
  "2": "[Translation of Basic Feelings]",
  "3": "[Translation of Expressing Affection (Advanced Edition)]",
  "4": "[Translation of Expressing Surprises and Reactions]",
  "5": "[Translation of Time and Telling Time]",
  "6": "[Translation of Months of the Year]",
  "7": "[Translation of Days of the Week]"
}}

Return ONLY valid JSON. No markdown, no explanations."""

            response = self.gemini_client.models.generate_content(
                model="gemma-3-27b-it",
                contents=prompt
            )

            result_text = response.text.strip()

            # Remove markdown code blocks if present
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()

            titles_data = json.loads(result_text)
            # Convert string keys to int keys
            titles = {int(k): v for k, v in titles_data.items()}

            return ModuleTitlesResponse(
                success=True,
                message=f"Successfully retrieved module titles for {language_code}",
                titles=titles
            )

        except json.JSONDecodeError as e:
            return ModuleTitlesResponse(
                success=False,
                message=f"Failed to parse AI response: {str(e)}",
                titles=None
            )
        except Exception as e:
            return ModuleTitlesResponse(
                success=False,
                message=f"Error getting module titles: {str(e)}",
                titles=None
            )

    async def generate(self, request: Chapter2GenerationRequest) -> Chapter2Response:
        """Generate specified modules for Chapter 2"""
        try:
            language_code = request.target_language
            
            # Determine which modules to generate
            if request.module_titles:
                # First, get the translated titles to match against
                titles_request = ModuleTitlesRequest(target_language=language_code)
                titles_response = await self.get_module_titles(titles_request)
                
                if not titles_response.success:
                    return Chapter2Response(
                        success=False,
                        message=f"Failed to get module titles: {titles_response.message}",
                        chapter=None
                    )
                
                # Match user-provided titles to module numbers using fuzzy matching
                translated_titles = titles_response.titles
                title_to_number = {v.lower(): k for k, v in translated_titles.items()}
                all_titles = list(title_to_number.keys())
                
                module_nums = []
                matched_titles = {}
                
                for user_title in request.module_titles:
                    user_title_lower = user_title.lower()
                    
                    # Try exact match first
                    if user_title_lower in title_to_number:
                        module_num = title_to_number[user_title_lower]
                        module_nums.append(module_num)
                        matched_titles[user_title] = translated_titles[module_num]
                    else:
                        # Try fuzzy matching
                        matches = get_close_matches(user_title_lower, all_titles, n=1, cutoff=0.6)
                        if matches:
                            matched_title = matches[0]
                            module_num = title_to_number[matched_title]
                            module_nums.append(module_num)
                            matched_titles[user_title] = translated_titles[module_num]
                        else:
                            return Chapter2Response(
                                success=False,
                                message=f"Could not match title '{user_title}' to any module. Available titles: {list(translated_titles.values())}",
                                chapter=None
                            )
                
                module_nums = sorted(set(module_nums))  # Remove duplicates and sort
            else:
                # Generate all modules if none specified
                module_nums = list(range(1, 8))
                matched_titles = None
            
            # Build the prompt for requested modules only
            prompt = self._build_prompt(language_code, module_nums)
            
            response = self.gemini_client.models.generate_content(
                model="gemma-3-27b-it",
                contents=prompt
            )

            result_text = response.text.strip()

            # Remove markdown code blocks if present
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()

            chapter_data = json.loads(result_text)
            chapter = Chapter2Content(**chapter_data)

            if matched_titles:
                module_list = ", ".join([f"{matched_titles.get(title, MODULE_NAMES[num])}" for num, title in zip(module_nums, request.module_titles)])
            else:
                module_list = ", ".join([MODULE_NAMES[num] for num in module_nums])
                
            return Chapter2Response(
                success=True,
                message=f"Successfully generated modules for {language_code}: {module_list}",
                chapter=chapter,
                generation_info={
                    "model": "gemma-3-27b-it", 
                    "modules_count": len(chapter.modules),
                    "requested_modules": module_nums,
                    "matched_titles": matched_titles
                }
            )

        except json.JSONDecodeError as e:
            return Chapter2Response(
                success=False,
                message=f"Failed to parse AI response: {str(e)}",
                chapter=None
            )
        except Exception as e:
            return Chapter2Response(
                success=False,
                message=f"Error generating Chapter 2: {str(e)}",
                chapter=None
            )
    
    def _build_prompt(self, language_name: str, module_nums: list) -> str:
        """Build prompt for specified modules only"""
        
        module_specs = {
            1: {
                "title": "Places and Locations",
                "vocab": ["School", "Home", "Restaurant", "Park", "Hospital", 
                         "Market/Store", "Library", "Office", "Street", "City/Town"],
                "grammar_topic": "Prepositions of Place",
                "grammar_desc": f"Explain how {language_name} expresses location (at, in, on) and basic directional prepositions"
            },
            2: {
                "title": "Basic Feelings",
                "vocab": ["Happy", "Sad", "Angry", "Tired", "Excited", 
                         "Bored", "Worried", "Calm", "Scared/Afraid", "Surprised"],
                "grammar_topic": "Expressing Emotions and States",
                "grammar_desc": f"Show how to describe feelings and emotional states in {language_name}, including verb forms for 'I feel...' or 'I am...'"
            },
            3: {
                "title": "Expressing Affection (Advanced Edition)",
                "vocab": ["I love you", "I care about you", "You're special", "I miss you", "I appreciate you",
                         "You mean a lot to me", "I adore you", "You make me happy", "I treasure you", "I'm grateful for you"],
                "grammar_topic": "Expressing Deep Emotions",
                "grammar_desc": f"Explain how {language_name} conveys affection and emotional attachment, including any cultural nuances"
            },
            4: {
                "title": "Expressing Surprises and Reactions",
                "vocab": ["Wow!", "Really?", "Amazing!", "I can't believe it!", "That's incredible!",
                         "How surprising!", "No way!", "Seriously?", "Unbelievable!", "Oh my!"],
                "grammar_topic": "Exclamations and Interjections",
                "grammar_desc": f"Show how to express surprise, shock, and strong reactions naturally in {language_name}"
            },
            5: {
                "title": "Time and Telling Time",
                "vocab": ["What time is it?", "Hour", "Minute", "O'clock", "Half past",
                         "Quarter past", "Quarter to", "Morning", "Afternoon", "Evening/Night"],
                "grammar_topic": "Time Expressions",
                "grammar_desc": f"Explain how to tell time in {language_name}, including different time formats and common time-related phrases"
            },
            6: {
                "title": "Months of the Year",
                "vocab": ["January", "February", "March", "April", "May", "June",
                         "July", "August", "September", "October"],
                "grammar_topic": "Temporal Expressions with Months",
                "grammar_desc": f"Show how months are used in {language_name} with dates and temporal expressions (in January, during March, etc.)"
            },
            7: {
                "title": "Days of the Week",
                "vocab": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                         "Saturday", "Sunday", "Today", "Tomorrow", "Yesterday"],
                "grammar_topic": "Time Markers and Schedule Talk",
                "grammar_desc": f"Explain how to talk about schedules, routines, and appointments using days of the week in {language_name}"
            }
        }
        
        prompt_parts = [f"""Generate Chapter 2 modules (A1 → A2 level) for learning {language_name}.

Topic: Action, Time and Place

**CRITICAL INSTRUCTION**: Do not generate any greetings, introductions, or phrases that include personal names, placeholders like [your name], or similar personal references. Focus only on the educational content specified.

Generate the following modules. Each module contains:
- Vocabulary: Exactly 10 items with English word/phrase and translation
- Grammar: One grammar concept with topic, concise 2-3 sentence explanation, and 2-3 examples

"""]
        
        for num in module_nums:
            spec = module_specs[num]
            vocab_list = "\n".join([f"{i+1}. {item}" for i, item in enumerate(spec["vocab"])])
            
            prompt_parts.append(f"""
# MODULE {num}: {spec['title']}
**Vocabulary (10 items):**
{vocab_list}

**Grammar Concept:**
- Topic: "{spec['grammar_topic']}"
- {spec['grammar_desc']}
- Provide 2-3 examples

---
""")
        
        # Add JSON format instruction
        json_example_modules = ",\n    ".join([f"""{{
      "module_number": {num},
      "title": "{module_specs[num]['title']}",
      "vocabulary": [
        {{"number": 1, "english": "{module_specs[num]['vocab'][0]}", "target": "[TRANSLATION]"}},
        {{"number": 2, "english": "{module_specs[num]['vocab'][1]}", "target": "[TRANSLATION]"}},
        ...all 10 items
      ],
      "grammar": {{
        "topic": "{module_specs[num]['grammar_topic']}",
        "requirement": "[2-3 sentence explanation]",
        "examples": ["[EXAMPLE 1]", "[EXAMPLE 2]", "[EXAMPLE 3]"]
      }}
    }}""" for num in module_nums])
        
        prompt_parts.append(f"""
Respond with valid JSON in this exact format:
{{
  "modules": [
    {json_example_modules}
  ]
}}

Return ONLY valid JSON. No markdown, no explanations.""")
        
        return "".join(prompt_parts)
