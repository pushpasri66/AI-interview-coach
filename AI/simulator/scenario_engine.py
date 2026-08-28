import re
from typing import Dict, Any


class ScenarioEngine:
    """Parses and normalizes candidate career simulation scenarios."""

    SCENARIO_KEYWORDS = {
        "certification": ["cert", "certification", "certified", "aws certified", "cka", "ccna", "exam", "credential"],
        "apply_jobs": ["apply", "job", "jobs", "application", "applications", "faang", "startup", "recruiter", "resume submission"],
        "build_project": ["project", "build", "pipeline", "microservice", "app", "fullstack", "clone"],
        "improve_interview": ["interview", "mock", "score", "communication", "behavioral", "star", "confidence"],
        "change_role": ["switch", "pivot", "role", "transition", "become", "change career"],
        "learn_skill": ["learn", "study", "master", "course", "docker", "aws", "python", "sql", "pytorch", "react", "kubernetes"]
    }

    def infer_scenario_type(self, scenario_title: str, user_specified_type: str = "") -> str:
        """Determines scenario type from explicit parameter or contextual heuristics."""
        if user_specified_type and user_specified_type in [
            "learn_skill", "certification", "build_project", "improve_interview", "change_role", "apply_jobs"
        ]:
            return user_specified_type

        norm = scenario_title.lower().strip()
        for s_type, keywords in self.SCENARIO_KEYWORDS.items():
            for k in keywords:
                if re.search(r"\b" + re.escape(k) + r"\b", norm):
                    return s_type

        return "learn_skill"

