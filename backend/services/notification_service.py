class NotificationService:
    """Service generating personalized progress notifications and achievement alerts."""

    def get_candidate_notifications(self, user_id: int) -> list:
        """Generates dynamic notifications based on candidate activity."""
        notifications = [
            {
                "title": "Confidence Score Growth",
                "message": "Your confidence score improved by 15%. Continue practicing technical interviews.",
                "category": "success",
                "timestamp": "Just now"
            },
            {
                "title": "New Career Recommendation Available",
                "message": "AI Engine matched your profile 87% with 'Machine Learning Engineer'.",
                "category": "info",
                "timestamp": "1 hour ago"
            },
            {
                "title": "Skill Gap Identified",
                "message": "Consider adding Docker and MLOps to your 4-month roadmap.",
                "category": "warning",
                "timestamp": "1 day ago"
            }
        ]
        return notifications
