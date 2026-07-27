import unittest
from AI.llm.llm_interviewer import LLMInterviewer
from AI.llm.prompt_manager import PromptManager


class TestLLMEngine(unittest.TestCase):
    """Unit tests for Phase 7 LLM Conversational Interviewer & Prompts."""

    def test_01_prompt_manager(self):
        """Test prompt manager system personas."""
        pm = PromptManager()
        hr_prompt = pm.get_system_prompt("hr")
        self.assertIn("Senior HR Recruiter", hr_prompt)

        google_prompt = pm.get_system_prompt("technical", "Google")
        self.assertIn("Google", google_prompt)

    def test_02_llm_interviewer_contextual_followups(self):
        """Test context-aware dynamic follow-up questioning."""
        interviewer = LLMInterviewer("technical")
        resp = interviewer.process_candidate_answer(
            current_question="What projects have you built recently?",
            candidate_answer="I created a crop disease prediction model using PyTorch and CNN architectures."
        )

        self.assertIn("cnn", resp["ai_response"].lower())
        self.assertIn("ai_response", resp)


if __name__ == "__main__":
    unittest.main()
