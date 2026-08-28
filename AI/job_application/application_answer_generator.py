from typing import Dict, Any, List


class ApplicationAnswerGenerator:
    """Generates tailored, high-converting answers to standard job application screening questions."""

    def generate_screening_answers(
        self,
        company_name: str,
        target_role: str,
        skills: List[str],
        top_project: str,
        years_experience: str = "2+ years"
    ) -> List[Dict[str, Any]]:
        """Generates comprehensive screening question-answer pairs."""
        primary_skill = skills[0] if skills else "Software Engineering"
        secondary_skill = skills[1] if len(skills) > 1 else "Full Stack Architecture"

        answers = [
            {
                "question": f"Why are you interested in joining {company_name}?",
                "category": "Company Motivation",
                "answer": (
                    f"I have closely followed {company_name}'s engineering advancements and culture of innovation. "
                    f"The opportunity to apply my expertise in {primary_skill} to solve complex, high-scale challenges "
                    f"aligns directly with my long-term technical aspirations. I want to build systems that create meaningful impact alongside a world-class team."
                ),
                "key_talking_points": ["Company mission alignment", "Technical scale interest", "Continuous learning commitment"]
            },
            {
                "question": f"Describe a significant technical achievement or project relevant to the {target_role} role.",
                "category": "Technical Achievement",
                "answer": (
                    f"My most significant accomplishment was engineering '{top_project}'. I led the architectural design, "
                    f"implementing asynchronous processing with {primary_skill} and optimizing query latency by over 35%. "
                    f"I established automated CI/CD pipelines with comprehensive unit and integration test coverage, ensuring zero downtime deployments."
                ),
                "key_talking_points": ["Quantifiable performance gain (35%)", "Modular architecture", "Automated CI/CD testing"]
            },
            {
                "question": f"Why are you the ideal candidate for this {target_role} position?",
                "category": "Role Fit",
                "answer": (
                    f"I bring a proven blend of hands-on expertise in {primary_skill} and {secondary_skill}, combined with a structured problem-solving approach. "
                    f"Beyond writing clean, testable code, I excel at cross-functional communication, rapid adaptability to new frameworks, "
                    f"and proactively eliminating technical debt."
                ),
                "key_talking_points": ["Core technical proficiency", "Collaborative ownership", "Proactive quality assurance"]
            },
            {
                "question": "How do you approach tight deadlines and shifting technical priorities?",
                "category": "Work Ethic & Prioritization",
                "answer": (
                    "I begin by decomposing requirements into high-value atomic milestones, establishing transparency with stakeholders, "
                    "and mitigating architectural risks early. By maintaining strict testing standards and iterative releases, "
                    "I ensure velocity without sacrificing system reliability."
                ),
                "key_talking_points": ["Milestone decomposition", "Stakeholder communication", "Quality vs velocity balance"]
            }
        ]

        return answers
