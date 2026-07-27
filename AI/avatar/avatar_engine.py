from AI.avatar.facial_animation import FacialAnimation
from AI.avatar.lip_sync import LipSyncEngine
from AI.avatar.avatar_response import AvatarResponse


class AvatarEngine:
    """Master AI Avatar engine orchestrating facial animation, lip synchronization, and avatar responses."""

    def __init__(self):
        self.animation = FacialAnimation()
        self.lip_sync = LipSyncEngine()
        self.response_builder = AvatarResponse()

    def process_avatar_speech(self, text: str) -> dict:
        """Processes AI interviewer speech text and generates visemes and animation frames."""
        visemes = self.lip_sync.generate_visemes(text)
        anim_state = self.animation.get_animation_states(is_speaking=True)
        return self.response_builder.build_avatar_payload(text, visemes, anim_state)
