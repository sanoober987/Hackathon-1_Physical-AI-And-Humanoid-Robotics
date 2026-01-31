from typing import Dict, List, Any
import os
from dotenv import load_dotenv
from openai import OpenAI
import asyncio

load_dotenv()

class TranslationService:
    def __init__(self):
        # Initialize OpenAI client for translation
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not found. Translation will return original text.")
            self.openai_client = None
        else:
            self.openai_client = OpenAI(api_key=api_key)

    def translate_text(self, text: str, target_lang: str = "ur", source_lang: str = "en") -> str:
        """
        Translate text to target language using OpenAI
        """
        if target_lang == source_lang:
            return text

        # If OpenAI client is not available, return original text with warning
        if not self.openai_client:
            print(f"Warning: OpenAI client not available, returning original text for translation from {source_lang} to {target_lang}")
            return text

        # Define language codes
        lang_codes = {
            "en": "English",
            "ur": "Urdu"
        }

        target_language = lang_codes.get(target_lang, target_lang)
        source_language = lang_codes.get(source_lang, source_language)

        if target_lang == "ur":
            # Special handling for Urdu translation
            prompt = f"""
Translate the following text from {source_language} to {target_language}.
Please provide an accurate translation that preserves the meaning and context.
The text is related to Physical AI and Humanoid Robotics concepts.

Text to translate:
{text}

Translation in {target_language}:
"""
        else:
            prompt = f"""
Translate the following text from {source_language} to {target_language}.
Please provide an accurate translation that preserves the meaning and context.

Text to translate:
{text}

Translation in {target_language}:
"""

        try:
            response = self.openai_client.chat.completions.create(
                model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": f"You are a professional translator specializing in technical content. Translate accurately between languages while preserving technical terminology and meaning. For Urdu translations, use proper Urdu script."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Translation error: {e}")
            return f"[TRANSLATION ERROR: {text}]"

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text
        """
        # This is a simplified implementation
        # In a production system, you might use a dedicated language detection library
        # For now, we'll assume English as default
        return "en"

    async def translate_batch(self, texts: List[str], target_lang: str = "ur") -> List[str]:
        """
        Translate multiple texts to target language
        """
        translations = []
        for text in texts:
            translation = self.translate_text(text, target_lang)
            translations.append(translation)
            # Small delay to avoid rate limits
            await asyncio.sleep(0.1)

        return translations