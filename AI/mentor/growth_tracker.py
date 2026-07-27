class GrowthTracker:
    """Tracks candidate technical and behavioral growth trajectory."""

    def calculate_growth_trend(self, historical_scores: list) -> dict:
        """Calculates growth percentage and trajectory status."""
        if not historical_scores:
            return {"growth_percentage": 0, "status": "Initial State", "trend": "flat"}

        first = historical_scores[0]
        latest = historical_scores[-1]
        diff = latest - first
        pct = int((diff / max(1, first)) * 100)

        return {
            "initial_score": first,
            "latest_score": latest,
            "growth_percentage": pct,
            "status": "Accelerating Growth" if pct > 15 else "Steady Progress",
            "trend": "upward" if diff >= 0 else "downward"
        }
