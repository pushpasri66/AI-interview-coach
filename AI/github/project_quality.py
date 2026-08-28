import re
from typing import Dict, Any, List


class ProjectQualityEvaluator:
    """Evaluates individual and aggregated repository quality, complexity, README completeness, and documentation."""

    def evaluate_readme(self, readme_content: str) -> Dict[str, Any]:
        """Scores README quality (0-100) based on structure, install steps, badges, and clarity."""
        if not readme_content or len(readme_content.strip()) < 30:
            return {
                "score": 35,
                "has_title": False,
                "has_installation": False,
                "has_usage": False,
                "has_badges": False,
                "has_architecture": False,
                "feedback": "README is empty or minimal. Add setup, usage, and architecture overview."
            }

        text = readme_content.lower()
        score = 40

        has_title = bool(re.search(r"^\s*#\s+", readme_content, re.MULTILINE))
        has_install = any(k in text for k in ["installation", "getting started", "setup", "quickstart", "pip install", "npm install"])
        has_usage = any(k in text for k in ["usage", "how to run", "example", "api reference", "commands"])
        has_badges = any(k in text for k in ["badge", "shields.io", "travis", "workflow", "build|passing", "license"])
        has_arch = any(k in text for k in ["architecture", "flowchart", "system design", "overview", "components", "diagram"])

        if has_title: score += 10
        if has_install: score += 15
        if has_usage: score += 15
        if has_badges: score += 10
        if has_arch: score += 10

        return {
            "score": min(100, score),
            "has_title": has_title,
            "has_installation": has_install,
            "has_usage": has_usage,
            "has_badges": has_badges,
            "has_architecture": has_arch
        }

    def evaluate_repository_complexity(self, repo_info: Dict[str, Any]) -> int:
        """Calculates project architectural complexity score (0-100)."""
        score = 50
        size_kb = repo_info.get("size", 100)
        stars = repo_info.get("stargazers_count", 0)
        forks = repo_info.get("forks_count", 0)
        has_description = bool(repo_info.get("description"))
        lang = repo_info.get("language") or "Other"

        # Codebase scale
        if size_kb > 5000: score += 15
        elif size_kb > 1000: score += 10
        elif size_kb > 200: score += 5

        # Social traction
        if stars > 10: score += 15
        elif stars > 2: score += 8

        if forks > 5: score += 10
        elif forks > 1: score += 5

        if has_description: score += 5
        if lang in ["Python", "TypeScript", "Go", "Rust", "C++", "Java"]: score += 5

        return min(100, max(30, score))
