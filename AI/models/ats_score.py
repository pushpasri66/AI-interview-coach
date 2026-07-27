import re


class ATSScoreCalculator:
    """Calculates a weighted 100-point ATS compliance score for candidate resumes."""

    ACTION_VERBS = [
        "built", "developed", "engineered", "implemented", "designed", "created",
        "architected", "optimized", "managed", "led", "launched", "automated",
        "refactored", "integrated", "scaled", "analyzed", "reduced", "increased"
    ]

    def compute_score(self, parsed_data: dict, raw_text: str) -> dict:
        """Computes comprehensive ATS score, category breakdowns, and color status."""
        
        # 1. Contact Information Score (Max 15 pts)
        contact_score = 0
        if parsed_data.get("email") != "Not Found": contact_score += 5
        if parsed_data.get("phone") != "Not Found": contact_score += 4
        if parsed_data.get("linkedin") != "Not Found": contact_score += 3
        if parsed_data.get("github") != "Not Found": contact_score += 3

        # 2. Technical & Soft Skills Score (Max 25 pts)
        tech_skills_count = len(parsed_data.get("technical_skills", []))
        soft_skills_count = len(parsed_data.get("soft_skills", []))
        
        skills_score = min(18, tech_skills_count * 2) + min(7, soft_skills_count * 2)

        # 3. Essential Resume Sections (Max 20 pts)
        sections_score = 0
        if parsed_data.get("experience"): sections_score += 6
        if parsed_data.get("education"): sections_score += 5
        if parsed_data.get("projects"): sections_score += 5
        if parsed_data.get("certifications") or parsed_data.get("achievements"): sections_score += 4

        # 4. Word Count & Readability Depth (Max 15 pts)
        word_count = parsed_data.get("word_count", 0)
        if 250 <= word_count <= 900:
            depth_score = 15
        elif 150 <= word_count < 250 or 900 < word_count <= 1400:
            depth_score = 10
        else:
            depth_score = 5

        # 5. Action Verbs Usage (Max 15 pts)
        text_lowered = raw_text.lower()
        matched_verbs = [verb for verb in self.ACTION_VERBS if re.search(r"\b" + verb + r"\b", text_lowered)]
        verbs_score = min(15, len(matched_verbs) * 3)

        # 6. Projects & Certifications Presence (Max 10 pts)
        proj_cert_score = 0
        if parsed_data.get("projects"): proj_cert_score += 5
        if parsed_data.get("certifications"): proj_cert_score += 5

        # Total Aggregate Score
        total_score = min(100, contact_score + skills_score + sections_score + depth_score + verbs_score + proj_cert_score)

        # Determine Color & Grade
        if total_score >= 80:
            color = "#10b981"  # Emerald Green
            grade = "Excellent"
            explanation = "Your resume is highly optimized for ATS filters and candidate screening software."
        elif total_score >= 60:
            color = "#f59e0b"  # Amber
            grade = "Good"
            explanation = "Your resume meets standard requirements but can be improved with missing keywords and action verbs."
        else:
            color = "#ef4444"  # Red
            grade = "Needs Improvement"
            explanation = "Your resume lacks key technical sections, contact details, or formatting structure required by ATS parsers."

        return {
            "overall_score": total_score,
            "grade": grade,
            "color": color,
            "explanation": explanation,
            "categories": {
                "contact_info": {"score": contact_score, "max": 15, "label": "Contact & Links"},
                "skills": {"score": skills_score, "max": 25, "label": "Technical & Soft Skills"},
                "sections": {"score": sections_score, "max": 20, "label": "Resume Sections"},
                "content_depth": {"score": depth_score, "max": 15, "label": "Content Depth & Length"},
                "action_verbs": {"score": verbs_score, "max": 15, "label": "Impact Action Verbs"},
                "projects_certs": {"score": proj_cert_score, "max": 10, "label": "Projects & Certifications"}
            }
        }
