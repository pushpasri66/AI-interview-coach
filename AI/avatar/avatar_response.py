class AvatarResponse:
    """Formats avatar payload containing speech audio, visemes, and animation states."""

    def build_avatar_payload(self, spoken_text: str, visemes: list, animation_state: dict) -> dict:
        """Builds structured avatar response payload."""
        return {
            "spoken_text": spoken_text,
            "visemes": visemes,
            "animation": animation_state,
            "status": "active"
        }
