"""Chapter 3 Service - Family and Relationships (A2 → B1)"""
import json
from difflib import get_close_matches
import google.genai as genai
from app.core.config import settings
from app.services.lesson.chapters.chapter3.chapter3_schema import (
    Chapter3GenerationRequest,
    Chapter3Response,
    Chapter3Content,
    ModuleContent,
    MODULE_NAMES,
    ModuleTitlesRequest,
    ModuleTitlesResponse
)


class Chapter3Service:
    """Service for generating complete Chapter 3 with all 3 modules"""

    def __init__(self):
        """Initialize the Gemini client"""
        self.gemini_client = genai.Client(api_key=settings.get_api_key())

    async def get_module_titles(self, request: ModuleTitlesRequest) -> ModuleTitlesResponse:
        """Get all module titles translated to target language"""
        try:
            language_code = request.target_language
            
            prompt = f"""Translate the following 3 module titles into {language_code}.

Module titles in English:
1. Identify family members
2. Use possessive pronouns correctly
3. Introduce other people

Respond with ONLY a JSON object mapping module numbers to translated titles:
{{
  "1": "[Translation of Identify family members]",
  "2": "[Translation of Use possessive pronouns correctly]",
  "3": "[Translation of Introduce other people]"
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

    async def generate(self, request: Chapter3GenerationRequest) -> Chapter3Response:
        """Generate specified modules for Chapter 3"""
        try:
            language_code = request.target_language
            
            # Determine which modules to generate
            if request.module_titles:
                # First, get the translated titles to match against
                titles_request = ModuleTitlesRequest(target_language=language_code)
                titles_response = await self.get_module_titles(titles_request)
                
                if not titles_response.success:
                    return Chapter3Response(
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
                            return Chapter3Response(
                                success=False,
                                message=f"Could not match title '{user_title}' to any module. Available titles: {list(translated_titles.values())}",
                                chapter=None
                            )
                
                module_nums = sorted(set(module_nums))  # Remove duplicates and sort
            else:
                # Generate all modules if none specified
                module_nums = list(range(1, 4))
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
            chapter = Chapter3Content(**chapter_data)

            if matched_titles:
                module_list = ", ".join([f"{matched_titles.get(title, MODULE_NAMES[num])}" for num, title in zip(module_nums, request.module_titles)])
            else:
                module_list = ", ".join([MODULE_NAMES[num] for num in module_nums])
                
            return Chapter3Response(
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
            return Chapter3Response(
                success=False,
                message=f"Failed to parse AI response: {str(e)}",
                chapter=None
            )
        except Exception as e:
            return Chapter3Response(
                success=False,
                message=f"Error generating Chapter 3: {str(e)}",
                chapter=None
            )
    
    def _build_prompt(self, language_name: str, module_nums: list) -> str:
        """Build prompt for specified modules only"""
        
        module_specs = {
            1: {
                "title": "Identify family members",
                "vocab": ["Grandfather", "Grandmother", "Uncle", "Aunt", "Cousin (male)", 
                         "Cousin (female)", "Nephew", "Niece", "In-laws", "Relatives"],
                "grammar_topic": "Extended Family Vocabulary and Relationships",
                "grammar_desc": f"Explain how {language_name} describes extended family relationships, including any gender distinctions or formal/informal variations"
            },
            2: {
                "title": "Use possessive pronouns correctly",
                "vocab": ["My", "Your (singular)", "His", "Her", "Our", 
                         "Your (plural)", "Their", "Mine", "Yours", "Theirs"],
                "grammar_topic": "Possessive Pronouns and Determiners",
                "grammar_desc": f"Show the difference between possessive determiners (my, your) and possessive pronouns (mine, yours) in {language_name}, and how they agree with nouns"
            },
            3: {
                "title": "Introduce other people",
                "vocab": ["This is my brother", "I'd like you to meet my colleague", "Meet my friend Anna", "Let me introduce my teacher", "Have you met my sister?",
                         "Do you know my parents?", "Allow me to introduce my boss", "I'd like to introduce you to my neighbor", "Say hello to my classmate", "You should meet my cousin"],
                "grammar_topic": "Introduction Formulas and Social Registers",
                "grammar_desc": f"Explain formal vs informal introduction phrases in {language_name}, including appropriate contexts for each level of formality"
            }
        }
        
        prompt_parts = [f"""Generate Chapter 3 modules (A2 → B1 level) for learning {language_name}.

Topic: Family and Relationships

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
