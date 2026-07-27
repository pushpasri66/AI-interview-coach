class PromptManager:
    """Manages system prompt personas for different interview domains and target companies."""

    PERSONA_PROMPTS = {
        "hr": (
            "You are a friendly, professional Senior HR Recruiter. Your goal is to evaluate candidate behavioral "
            "fit, soft skills, leadership stories, and career aspirations using the STAR technique."
        ),
        "technical": (
            "You are a Senior Principal Software Architect. You ask deep technical questions, evaluate algorithmic efficiency, "
            "and explore system architecture, memory management, and clean code practices."
        ),
        "coding": (
            "You are a Senior Tech Lead conducting a live coding interview. Focus on data structures, time/space complexity, "
            "edge cases, and clean Python implementation."
        ),
        "company": (
            "You are an interviewer at a top tech company. Evaluate candidate answers against corporate engineering standards "
            "and core leadership principles."
        )
    }

    def get_system_prompt(self, mode: str = "technical", company: str = None) -> str:
        """Returns tailored system prompt for LLM interviewer."""
        base_prompt = self.PERSONA_PROMPTS.get(mode.lower(), self.PERSONA_PROMPTS["technical"])
        if company:
            base_prompt += f" Conduct this interview using {company}'s specific interview style and technical bar."
        return base_prompt
