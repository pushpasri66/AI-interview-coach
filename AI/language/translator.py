class RegionalTranslator:
    """Translates interview questions and responses between English, Telugu, Hindi, and Tamil."""

    SAMPLE_TRANSLATIONS = {
        "te": {
            "Tell me about yourself.": "మీ గురించి వివరించండి (Tell me about yourself).",
            "What is Python?": "పైథాన్ అంటే ఏమిటి (What is Python)?"
        },
        "hi": {
            "Tell me about yourself.": "अपने बारे में बताइए (Tell me about yourself).",
            "What is Python?": "पायथन क्या है (What is Python)?"
        },
        "ta": {
            "Tell me about yourself.": "உங்களைப் பற்றி சொல்லுங்கள் (Tell me about yourself).",
            "What is Python?": "பைத்தான என்றால் என்ன (What is Python)?"
        }
    }

    def translate_question(self, question_text: str, target_lang: str = "en") -> str:
        """Translates question text to target language."""
        if target_lang == "en" or not question_text:
            return question_text

        trans_map = self.SAMPLE_TRANSLATIONS.get(target_lang, {})
        return trans_map.get(question_text, f"[{target_lang.upper()}] {question_text}")
