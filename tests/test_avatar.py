import unittest
from AI.avatar.avatar_engine import AvatarEngine
from AI.avatar.lip_sync import LipSyncEngine
from AI.avatar.facial_animation import FacialAnimation


class TestAIAvatarEngine(unittest.TestCase):
    """Unit tests for Phase 7 AI Avatar Engine, Lip Sync, and Facial Animation."""

    def test_01_lip_sync_visemes(self):
        """Test audio viseme lip sync sequence generation."""
        engine = LipSyncEngine()
        visemes = engine.generate_visemes("Hello welcome to the technical interview.")
        self.assertEqual(len(visemes), 6)
        self.assertIn("viseme", visemes[0])

    def test_02_facial_animation_states(self):
        """Test facial animation states."""
        anim = FacialAnimation()
        state = anim.get_animation_states(is_speaking=True)
        self.assertTrue(state["head_nod"])
        self.assertEqual(state["smile_intensity"], 0.45)

    def test_03_avatar_engine_speech_processing(self):
        """Test master AvatarEngine payload generator."""
        avatar = AvatarEngine()
        payload = avatar.process_avatar_speech("Please describe your project experience.")
        self.assertIn("spoken_text", payload)
        self.assertIn("visemes", payload)


if __name__ == "__main__":
    unittest.main()
