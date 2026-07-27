import unittest
from AI.language.language_detector import LanguageDetector
from AI.language.translator import RegionalTranslator
from AI.language.voice_language import VoiceLanguageManager


class TestMultiLanguageSupport(unittest.TestCase):
    """Unit tests for Phase 7 Multi-Language Support (English, Telugu, Hindi, Tamil)."""

    def test_01_language_detection(self):
        """Test language detection for English and regional scripts."""
        detector = LanguageDetector()
        res_en = detector.detect_language("What is Python?")
        self.assertEqual(res_en["lang_code"], "en")

        res_te = detector.detect_language("మీ గురించి వివరించండి")
        self.assertEqual(res_te["lang_code"], "te")

    def test_02_regional_translator(self):
        """Test regional question translation."""
        translator = RegionalTranslator()
        trans_te = translator.translate_question("Tell me about yourself.", "te")
        self.assertIn("మీ గురించి వివరించండి", trans_te)

    def test_03_voice_language_locales(self):
        """Test voice locale manager."""
        v_mgr = VoiceLanguageManager()
        self.assertEqual(v_mgr.get_speech_locale("te"), "te-IN")
        self.assertEqual(v_mgr.get_speech_locale("hi"), "hi-IN")


if __name__ == "__main__":
    unittest.main()
