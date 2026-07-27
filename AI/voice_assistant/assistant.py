from AI.voice_assistant.speech_to_text import VoiceSpeechToText
from AI.voice_assistant.text_to_speech import VoiceTextToSpeech


class VoiceAssistant:
    """Multilingual AI Voice Assistant providing voice navigation, career guidance, and interview commands."""

    def __init__(self):
        self.stt = VoiceSpeechToText()
        self.tts = VoiceTextToSpeech()

    def process_voice_command(self, voice_text: str, lang_code: str = "en") -> dict:
        """Processes candidate voice command and responds with voice TTS payload."""
        cmd = voice_text.lower() if voice_text else ""

        if "start interview" in cmd or "mock interview" in cmd:
            response_text = "Navigating to AI Mock Interview setup room."
            action = "navigate_interview"
        elif "career advice" in cmd or "mentor" in cmd:
            response_text = "Opening your personal AI Career Mentor dashboard."
            action = "navigate_mentor"
        elif "resume" in cmd:
            response_text = "Navigating to AI Resume Builder & ATS Engine."
            action = "navigate_resume"
        else:
            response_text = f"I am your AI Career Assistant. How can I assist your job preparation today?"
            action = "info"

        voice_payload = self.tts.synthesize_voice_audio(response_text, lang_code)

        return {
            "user_command": voice_text,
            "response_text": response_text,
            "action": action,
            "voice_audio": voice_payload
        }
