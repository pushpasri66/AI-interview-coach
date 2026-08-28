from typing import Dict, Any, List


class CoverLetterGenerator:
    """Generates personalized, high-impact cover letters tailored to target companies and job descriptions."""

    def generate_cover_letter(
        self,
        candidate_name: str,
        candidate_email: str,
        company_name: str,
        target_role: str,
        key_skills: List[str],
        top_project: str,
        job_description: str = ""
    ) -> str:
        """Constructs a professional, structured cover letter."""
        skills_formatted = ", ".join(key_skills[:4]) if key_skills else "modern software engineering practices"
        project_ref = f"developing '{top_project}'" if top_project else "building scalable software architectures"

        letter = f"""Dear Hiring Team at {company_name},

I am writing to express my strong enthusiasm for the {target_role} position at {company_name}. With hands-on experience in {skills_formatted} and a track record of delivering resilient, high-performance software systems, I am eager to contribute to {company_name}'s ongoing engineering mission and product innovation.

Throughout my technical journey, I have prioritized architectural clarity, code maintainability, and measurable impact. A key highlight of my work includes {project_ref}, where I designed modular microservices, optimized computational throughput, and implemented rigorous automated test suites. This experience strengthened my ability to translate complex business requirements into robust, production-ready software solutions.

What particularly excites me about {company_name} is your commitment to technical excellence and solving impactful challenges at scale. My proficiency with {key_skills[0] if key_skills else 'software development'} combined with my continuous drive for learning positions me to deliver immediate value to your engineering team.

I welcome the opportunity to discuss how my technical skill set, problem-solving mindset, and dedication align with your goals for the {target_role} team. Thank you for your time and consideration.

Sincerely,

{candidate_name}
{candidate_email}
"""
        return letter.strip()
