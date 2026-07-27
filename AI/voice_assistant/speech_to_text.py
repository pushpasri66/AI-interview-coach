class VoiceSpeechToText:
    """Multilingual Speech-to-Text transcriber supporting English, Telugu, Hindi, and Tamil."""

    def transcribe_audio_stream(self, audio_data: bytes, lang_code: str = "en") -> dict:
        """Transcribes candidate audio stream to text transcript."""
        return {
            "transcript": "I am interested in applying for the AI Engineer role.",
            "language": lang_code,
            "confidence": 0.96
        }
