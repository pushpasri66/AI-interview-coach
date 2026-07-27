class FacialAnimation:
    """Computes facial expression frames (smile, blink, head nod) for AI interviewer avatar."""

    def get_animation_states(self, is_speaking: bool = False) -> dict:
        """Returns current animation frame state for avatar client rendering."""
        return {
            "eye_blink": False,
            "head_nod": is_speaking,
            "eyebrow_raise": False,
            "smile_intensity": 0.45 if is_speaking else 0.30
        }
