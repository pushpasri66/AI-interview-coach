class LanguageDetector:
    """Detects input language (English, Telugu, Hindi, Tamil) for candidate prompts and answers."""

    SUPPORTED_LANGUAGES = {
        "en": "English",
        "te": "Telugu",
        "hi": "Hindi",
        "ta": "Tamil"
    }

    def detect_language(self, text: str) -> dict:
        """Detects language code and language name."""
        if not text or not text.strip():
            return {"lang_code": "en", "lang_name": "English"}

        # Check script / unicode ranges or keywords
        has_telugu = any('\u0c00' <= char <= '\u0c7f' for char in text)
        has_hindi = any('\u0900' <= char <= '\u097f' for char in text)
        has_tamil = any('\u0b80' <= char <= '\u0bff' for char in text)

        if has_telugu:
            return {"lang_code": "te", "lang_name": "Telugu"}
        elif has_hindi:
            return {"lang_code": "hi", "lang_name": "Hindi"}
        elif has_tamil:
            return {"lang_code": "ta", "lang_name": "Tamil"}
        else:
            return {"lang_code": "en", "lang_name": "English"}
