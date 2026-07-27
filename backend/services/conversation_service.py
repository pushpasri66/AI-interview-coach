from backend.database import db
from backend.models.conversation import Conversation


class ConversationService:
    """Service storing and retrieving conversational Q&A history."""

    def save_exchange(self, user_id: int, interview_id: int, question: str, answer: str, ai_response: str) -> Conversation:
        """Saves conversational exchange in database."""
        rec = Conversation(
            user_id=user_id,
            interview_id=interview_id,
            question=question,
            answer=answer,
            ai_response=ai_response
        )
        db.session.add(rec)
        db.session.commit()
        return rec

    def get_interview_history(self, interview_id: int) -> list:
        """Retrieves conversational exchanges for an interview session."""
        return Conversation.query.filter_by(interview_id=interview_id).order_by(Conversation.timestamp.asc()).all()
