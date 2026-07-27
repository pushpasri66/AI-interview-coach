import unittest
from AI.voice_assistant.assistant import VoiceAssistant
from AI.voice_assistant.speech_to_text import VoiceSpeechToText
from AI.voice_assistant.text_to_speech import VoiceTextToSpeech


class TestVoiceAssistant(unittest.TestCase):
    """Unit tests for Phase 8 Multilingual Voice AI Assistant."""

    def test_01_voice_assistant_commands(self):
        """Test processing voice commands and navigation actions."""
        assistant = VoiceAssistant()
        res = assistant.process_voice_command("Start mock interview", "en")
        self.assertEqual(res["action"], "navigate_interview")

        res_mentor = assistant.process_voice_command("I need career advice", "en")
        self.assertEqual(res_mentor["action"], "navigate_mentor")

    def test_02_stt_and_tts(self):
        """Test STT transcription and TTS speech synthesis."""
        stt = VoiceSpeechToText()
        stt_res = stt.transcribe_audio_stream(b"audio", "te")
        self.assertEqual(stt_res["language"], "te")

        tts = VoiceTextToSpeech()
        tts_res = tts.synthesize_voice_audio("Hello", "hi")
        self.assertEqual(tts_res["audio_format"], "mp3")


if __name__ == "__main__":
    unittest.main()
