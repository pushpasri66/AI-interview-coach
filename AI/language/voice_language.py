class VoiceLanguageManager:
    """Manages multi-language voice synthesis locales for English, Telugu, Hindi, and Tamil."""

    VOICE_LOCALES = {
        "en": "en-US",
        "te": "te-IN",
        "hi": "hi-IN",
        "ta": "ta-IN"
    }

    def get_speech_locale(self, lang_code: str = "en") -> str:
        """Returns locale string for gTTS / Web Speech API."""
        return self.VOICE_LOCALES.get(lang_code.lower(), "en-US")
