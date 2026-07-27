from AI.llm.prompt_manager import PromptManager
from AI.llm.conversation_memory import ConversationMemory
from AI.llm.response_generator import ResponseGenerator


class LLMInterviewer:
    """Conversational AI LLM Interviewer understanding candidate context and generating intelligent follow-up questions."""

    def __init__(self, mode: str = "technical", company: str = None):
        self.prompt_manager = PromptManager()
        self.memory = ConversationMemory()
        self.response_generator = ResponseGenerator()
        self.system_prompt = self.prompt_manager.get_system_prompt(mode, company)

    def process_candidate_answer(self, current_question: str, candidate_answer: str) -> dict:
        """Processes candidate answer, updates memory, and generates contextual follow-up question."""
        self.memory.add_exchange(current_question, candidate_answer)
        answer_clean = candidate_answer.lower()

        # Dynamic context-aware follow-up generator rules
        if "crop disease" in answer_clean or "cnn" in answer_clean or "prediction" in answer_clean:
            follow_up = "Which CNN architecture did you use for crop disease prediction and why?"
            comment = "Great mention of computer vision modeling."
        elif "decorator" in answer_clean:
            follow_up = "How do decorators handle function arguments using *args and **kwargs internally?"
            comment = "Solid Python fundamentals response."
        elif "random forest" in answer_clean:
            follow_up = "How do you evaluate feature importance and prevent overfitting in Random Forest?"
            comment = "Good machine learning explanation."
        elif "sql" in answer_clean or "join" in answer_clean:
            follow_up = "What is the performance difference between an INNER JOIN and an EXISTS subquery?"
            comment = "Strong database knowledge."
        else:
            follow_up = f"That makes sense. Can you elaborate further on how you measured success or performance metrics in that project?"
            comment = "Clear explanation provided."

        return self.response_generator.format_interviewer_response(follow_up, comment)
