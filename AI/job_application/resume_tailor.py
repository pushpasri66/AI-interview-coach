import re
from typing import Dict, Any, List, Set


class ResumeTailor:
    """Tailors resume content, generates ATS keywords, and suggests targeted resume improvements."""

    COMMON_TECH_KEYWORDS = [
        "python", "javascript", "typescript", "react", "node.js", "docker", "kubernetes",
        "aws", "cloud", "sql", "postgresql", "mongodb", "redis", "fastapi", "flask",
        "machine learning", "deep learning", "pytorch", "ci/cd", "git", "rest apis",
        "microservices", "system design", "data structures", "algorithms", "linux"
    ]

    def extract_keywords_from_text(self, text: str) -> List[str]:
        """Extracts technical keywords present in job description or resume text."""
        norm = text.lower()
        extracted = []
        for kw in self.COMMON_TECH_KEYWORDS:
            if re.search(r"\b" + re.escape(kw) + r"\b", norm):
                extracted.append(kw.title())
        return extracted

    def tailor_resume_content(
        self,
        candidate_name: str,
        target_role: str,
        company_name: str,
        candidate_skills: List[str],
        job_description: str = "",
        existing_projects: List[str] = None
    ) -> Dict[str, Any]:
        """Generates tailored resume summary, optimized bullet points, and ATS keywords."""
        projects = existing_projects or ["Distributed Backend Service", "Full-Stack Web App"]
        top_project = projects[0] if projects else "Scalable Software Project"

        jd_keywords = self.extract_keywords_from_text(job_description) if job_description else ["Python", "SQL", "Docker", "REST APIs", "Git"]
        if len(jd_keywords) < 3:
            jd_keywords = ["Python", "Docker", "REST APIs", "SQL", "CI/CD", "System Design"]

        norm_candidate = {s.lower().strip() for s in candidate_skills}
        
        matched_kw = [kw for kw in jd_keywords if kw.lower() in norm_candidate]
        missing_kw = [kw for kw in jd_keywords if kw.lower() not in norm_candidate]

        coverage_pct = int((len(matched_kw) / max(1, len(jd_keywords))) * 100)
        match_score = min(98, max(45, int(coverage_pct * 0.65 + 30)))
        readiness = min(98, max(40, int(match_score * 0.90 + (10 if len(candidate_skills) >= 4 else 0))))

        # 1. Tailored Summary
        summary = (
            f"Results-driven {target_role} with proven proficiency in {', '.join(candidate_skills[:3]) if candidate_skills else 'software development'}. "
            f"Experienced in architecting modular systems, optimizing database latency, and delivering robust software solutions at {company_name}. "
            f"Dedicated to writing clean, maintainable code and accelerating engineering delivery through automated CI/CD and modern best practices."
        )

        # 2. Tailored Achievement Bullet Points
        bullet_points = [
            f"Architected and deployed {top_project}, implementing high-throughput asynchronous services using {candidate_skills[0] if candidate_skills else 'Python'} to reduce latency by 35%.",
            f"Designed and optimized relational SQL schema and caching tiers, supporting 10,000+ daily requests with 99.9% uptime.",
            f"Automated end-to-end testing and CI/CD pipelines, reducing manual deployment cycles from 45 minutes to under 5 minutes.",
            f"Collaborated cross-functionally with product and design teams to deliver key user-facing features ahead of schedule."
        ]

        # 3. Improvement Suggestions
        suggestions = []
        if missing_kw:
            suggestions.append(f"Incorporate missing target keywords into your skills and project sections: {', '.join(missing_kw[:3])}.")
        if coverage_pct < 75:
            suggestions.append("Add quantifiable metrics (e.g. '% latency reduction', 'user counts') to your top project bullet points.")
        suggestions.append(f"Position your primary project '{top_project}' prominently at the top of your experience section.")

        return {
            "tailored_summary": summary,
            "tailored_bullet_points": bullet_points,
            "highlighted_skills": candidate_skills[:8],
            "ats_keywords": {
                "matched_keywords": matched_kw,
                "missing_keywords": missing_kw,
                "target_keywords": jd_keywords,
                "keyword_coverage_percentage": coverage_pct
            },
            "job_match_score": match_score,
            "application_readiness": readiness,
            "missing_skills": missing_kw,
            "improvement_suggestions": suggestions
        }
