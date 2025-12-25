"""Chapter 4 Service - Expressing Gratitude and Apologies (B1 → B2)"""
import json
from difflib import get_close_matches
import google.genai as genai
from app.core.config import settings
from app.services.lesson.chapters.chapter4.chapter4_schema import (
    Chapter4GenerationRequest,
    Chapter4Response,
    Chapter4Content,
    ModuleContent,
    MODULE_NAMES,
    ModuleTitlesRequest,
    ModuleTitlesResponse
)


class Chapter4Service:
    """Service for generating complete Chapter 4 with all 3 modules"""

    def __init__(self):
        """Initialize the Gemini client"""
        self.gemini_client = genai.Client(api_key=settings.get_api_key())

    async def get_module_titles(self, request: ModuleTitlesRequest) -> ModuleTitlesResponse:
        """Get all module titles translated to target language"""
        try:
            language_code = request.target_language
            
            prompt = f"""Translate the following 3 module titles into {language_code}.

Module titles in English:
1. Express gratitude appropriately
2. Apologize formally or casually
3. Understand cultural values

Respond with ONLY a JSON object mapping module numbers to translated titles:
{{
  "1": "[Translation of Express gratitude appropriately]",
  "2": "[Translation of Apologize formally or casually]",
  "3": "[Translation of Understand cultural values]"
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

    async def generate(self, request: Chapter4GenerationRequest) -> Chapter4Response:
        """Generate specified modules for Chapter 4"""
        try:
            language_code = request.target_language
            
            # Determine which modules to generate
            if request.module_titles:
                # First, get the translated titles to match against
                titles_request = ModuleTitlesRequest(target_language=language_code)
                titles_response = await self.get_module_titles(titles_request)
                
                if not titles_response.success:
                    return Chapter4Response(
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
                            return Chapter4Response(
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
            chapter = Chapter4Content(**chapter_data)

            if matched_titles:
                module_list = ", ".join([f"{matched_titles.get(title, MODULE_NAMES[num])}" for num, title in zip(module_nums, request.module_titles)])
            else:
                module_list = ", ".join([MODULE_NAMES[num] for num in module_nums])
                
            return Chapter4Response(
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
            return Chapter4Response(
                success=False,
                message=f"Failed to parse AI response: {str(e)}",
                chapter=None
            )
        except Exception as e:
            return Chapter4Response(
                success=False,
                message=f"Error generating Chapter 4: {str(e)}",
                chapter=None
            )
    
    def _build_prompt(self, language_name: str, module_nums: list) -> str:
        """Build prompt for specified modules only"""
        
        module_specs = {
            1: {
                "title": "Express gratitude appropriately",
                "vocab": ["Thank you very much", "I really appreciate it", "I'm grateful for your help", "That's very kind of you", "I can't thank you enough",
                         "Many thanks", "I owe you one", "How thoughtful!", "I'm so thankful", "Much obliged"],
                "grammar_topic": "Expressions of Gratitude - Formal and Informal Register",
                "grammar_desc": f"Explain the different levels of formality in expressing gratitude in {language_name}, from casual thanks to deeply formal appreciation, including when to use each register"
            },
            2: {
                "title": "Apologize formally or casually",
                "vocab": ["I apologize", "I'm sorry", "My apologies", "Please forgive me", "I didn't mean to",
                         "Excuse me", "Pardon me", "I take full responsibility", "I regret that", "My bad"],
                "grammar_topic": "Apology Formulas and Responsibility Acknowledgment",
                "grammar_desc": f"Show how {language_name} distinguishes between formal and casual apologies, including expressions that acknowledge responsibility versus lighter expressions for minor mistakes"
            },
            3: {
                "title": "Understand cultural values",
                "vocab": ["Respect", "Humility", "Politeness", "Face-saving", "Indirect communication",
                         "Social harmony", "Hierarchy", "Obligation", "Reciprocity", "Honor"],
                "grammar_topic": "Cultural Context in Communication",
                "grammar_desc": f"Explain how {language_name} reflects cultural values in communication, including concepts like indirect speech, maintaining social harmony, and respecting hierarchy through language choice"
            }
        }
        
        prompt_parts = [f"""Generate Chapter 4 modules (B1 → B2 level) for learning {language_name}.

Topic: Expressing Gratitude and Apologies

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
