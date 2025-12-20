"""Chapter 1 Service - Merged single API for all 10 modules"""
import json
from difflib import get_close_matches
import google.genai as genai
from app.core.config import settings
from app.services.lesson.chapters.chapter1.chapter1_schema import (
    Chapter1GenerationRequest,
    Chapter1Response,
    Chapter1Content,
    ModuleContent,
    MODULE_NAMES,
    ModuleTitlesRequest,
    ModuleTitlesResponse
)


class Chapter1Service:
    """Service for generating complete Chapter 1 with all 10 modules"""

    def __init__(self):
        """Initialize the Gemini client"""
        self.gemini_client = genai.Client(api_key=settings.get_api_key())

    async def get_module_titles(self, request: ModuleTitlesRequest) -> ModuleTitlesResponse:
        """Get all module titles translated to target language"""
        try:
            language_code = request.target_language
            
            prompt = f"""Translate the following 10 module titles into {language_code}.

Module titles in English:
1. Essential Greetings
2. Self Introductions
3. Belongings
4. Family & Relationships
5. Basic Likes/Dislikes
6. Gratitude & Apologies
7. Numbers 1-10
8. Numbers 11-100
9. Colors
10. Review & Integration

Respond with ONLY a JSON object mapping module numbers to translated titles:
{{
  "1": "[Translation of Essential Greetings]",
  "2": "[Translation of Self Introductions]",
  "3": "[Translation of Belongings]",
  "4": "[Translation of Family & Relationships]",
  "5": "[Translation of Basic Likes/Dislikes]",
  "6": "[Translation of Gratitude & Apologies]",
  "7": "[Translation of Numbers 1-10]",
  "8": "[Translation of Numbers 11-100]",
  "9": "[Translation of Colors]",
  "10": "[Translation of Review & Integration]"
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

    async def generate(self, request: Chapter1GenerationRequest) -> Chapter1Response:
        """Generate specified modules for Chapter 1"""
        try:
            language_code = request.target_language
            
            # Determine which modules to generate
            if request.module_titles:
                # First, get the translated titles to match against
                titles_request = ModuleTitlesRequest(target_language=language_code)
                titles_response = await self.get_module_titles(titles_request)
                
                if not titles_response.success:
                    return Chapter1Response(
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
                            return Chapter1Response(
                                success=False,
                                message=f"Could not match title '{user_title}' to any module. Available titles: {list(translated_titles.values())}",
                                chapter=None
                            )
                
                module_nums = sorted(set(module_nums))  # Remove duplicates and sort
            else:
                # Generate all modules if none specified
                module_nums = list(range(1, 11))
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
            chapter = Chapter1Content(**chapter_data)

            if matched_titles:
                module_list = ", ".join([f"{matched_titles.get(title, MODULE_NAMES[num])}" for num, title in zip(module_nums, request.module_titles)])
            else:
                module_list = ", ".join([MODULE_NAMES[num] for num in module_nums])
                
            return Chapter1Response(
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
            return Chapter1Response(
                success=False,
                message=f"Failed to parse AI response: {str(e)}",
                chapter=None
            )
        except Exception as e:
            return Chapter1Response(
                success=False,
                message=f"Error generating Chapter 1: {str(e)}",
                chapter=None
            )
    
    def _build_prompt(self, language_name: str, module_nums: list) -> str:
        """Build prompt for specified modules only"""
        
        module_specs = {
            1: {
                "title": "Essential Greetings",
                "vocab": ["Good Morning", "Good Afternoon", "Good Evening", "Hello", "Goodbye", 
                         "See you later", "Good night", "How are you?", "I am fine", "And you?"],
                "grammar_topic": "Formal vs. Informal Registers",
                "grammar_desc": f"Explain how {language_name} distinguishes between talking to a friend vs. an elder/stranger"
            },
            2: {
                "title": "Self Introductions",
                "vocab": ["My name is...", "I am...", "I am from...", "Nice to meet you", "Pleased to meet you",
                         "This is...", "Student", "Teacher", "Country", "City"],
                "grammar_topic": f"The Verb 'to be' in {language_name}",
                "grammar_desc": "Explain how to form basic sentences with the verb 'to be' (I am, you are, he/she is)"
            },
            3: {
                "title": "Belongings",
                "vocab": ["Phone", "Bag", "Book", "Pen", "Wallet", "Keys", "Water", "This", "That", "Mine/Yours"],
                "grammar_topic": "Possessive Markers",
                "grammar_desc": f"Show how possession is expressed in {language_name} (e.g., my book, your phone, his keys)"
            },
            4: {
                "title": "Family & Relationships",
                "vocab": ["Mother", "Father", "Sister", "Brother", "Friend", "Family", "Husband", "Wife", "Child/Children", "Parents"],
                "grammar_topic": "Describing People Using Adjectives",
                "grammar_desc": f"Explain how adjectives are used with nouns in {language_name} (e.g., 'my older sister', 'kind friend')"
            },
            5: {
                "title": "Basic Likes/Dislikes",
                "vocab": ["Like", "Love", "Dislike", "Hate", "Food", "Music", "Sports", "Movies", "Reading", "Coffee/Tea"],
                "grammar_topic": "Verb Conjugation for Preferences",
                "grammar_desc": f"Show how 'like', 'love', 'dislike' verbs are used in {language_name} with different subjects"
            },
            6: {
                "title": "Gratitude & Apologies",
                "vocab": ["Thank you", "Thanks a lot", "You're welcome", "Sorry", "Excuse me", 
                         "I apologize", "No problem", "It's okay", "Please", "May I...?"],
                "grammar_topic": "Polite Request Forms",
                "grammar_desc": f"Explain how to make polite requests and responses in {language_name}"
            },
            7: {
                "title": "Numbers 1-10",
                "vocab": ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"],
                "grammar_topic": "Using Numbers with Nouns",
                "grammar_desc": f"Explain how numbers combine with nouns in {language_name} (e.g., counting objects, using counters/classifiers if applicable)"
            },
            8: {
                "title": "Numbers 11-100",
                "vocab": ["Eleven (11)", "Twenty (20)", "Thirty (30)", "Forty (40)", "Fifty (50)", 
                         "Sixty (60)", "Seventy (70)", "Eighty (80)", "Ninety (90)", "One hundred (100)"],
                "grammar_topic": "Number Formation Patterns",
                "grammar_desc": f"Explain how compound numbers are formed in {language_name} (e.g., 23 = twenty-three)"
            },
            9: {
                "title": "Colors",
                "vocab": ["Red", "Blue", "Green", "Yellow", "Black", "White", "Orange", "Purple", "Pink", "Brown"],
                "grammar_topic": "Adjective Placement",
                "grammar_desc": f"Show where color adjectives appear relative to nouns in {language_name} (before/after the noun)"
            },
            10: {
                "title": "Review & Integration",
                "vocab": ["Review item 1", "Review item 2", "Review item 3", "Review item 4", "Review item 5",
                         "Review item 6", "Review item 7", "Review item 8", "Review item 9", "Review item 10"],
                "grammar_topic": "Sentence Structure Review",
                "grammar_desc": "Provide an overview of basic sentence patterns covered in Chapter 1"
            }
        }
        
        prompt_parts = [f"""Generate Chapter 1 modules for learning {language_name}.

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
