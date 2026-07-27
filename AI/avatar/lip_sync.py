class LipSyncEngine:
    """Computes mouth viseme shapes for lip synchronizing AI avatar audio output."""

    def generate_visemes(self, text: str) -> list:
        """Generates viseme timestamp sequence for spoken text."""
        words = text.split() if text else []
        visemes = []
        for idx, word in enumerate(words):
            visemes.append({
                "time_offset_ms": idx * 300,
                "viseme": "open" if len(word) % 2 == 0 else "neutral",
                "word": word
            })
        return visemes
