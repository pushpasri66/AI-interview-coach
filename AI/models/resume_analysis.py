class ResumeAnalyzer:
    """Evaluates candidate resume to extract key strengths, weaknesses, and suggestions."""

    def analyze(self, parsed_data: dict, ats_results: dict) -> dict:
        """Generates structured lists of strengths, weaknesses, and actionable suggestions."""
        strengths = []
        weaknesses = []
        suggestions = []

        # 1. Contact & Profile Analysis
        if parsed_data.get("email") != "Not Found" and parsed_data.get("phone") != "Not Found":
            strengths.append("Complete primary contact information (Email and Phone Number).")
        else:
            weaknesses.append("Incomplete contact information (Missing Email or Phone).")
            suggestions.append("Ensure your primary phone number and professional email are clearly listed at the top.")

        if parsed_data.get("linkedin") != "Not Found":
            strengths.append("Professional LinkedIn profile link included.")
        else:
            weaknesses.append("Missing LinkedIn URL.")
            suggestions.append("Add your updated LinkedIn profile URL to increase recruiters' confidence.")

        if parsed_data.get("github") != "Not Found":
            strengths.append("GitHub repository link included for code verification.")
        else:
            weaknesses.append("Missing GitHub profile link.")
            suggestions.append("Add a GitHub profile link to showcase open-source contributions and portfolio projects.")

        # 2. Skills Evaluation
        tech_skills = parsed_data.get("technical_skills", [])
        if len(tech_skills) >= 6:
            strengths.append(f"Strong technical skill set detected ({len(tech_skills)} skills identified: {', '.join(tech_skills[:5])}).")
        else:
            weaknesses.append("Limited technical keywords detected for automated ATS screening.")
            suggestions.append("Incorporate more domain-specific technical skills, libraries, and frameworks into your skills section.")

        # 3. Experience & Projects
        projects = parsed_data.get("projects", [])
        if projects:
            strengths.append("Includes practical project experience detailing implementation tools.")
        else:
            weaknesses.append("No explicit projects section identified.")
            suggestions.append("Add 2-3 key technical projects highlighting your role, technologies used, and measurable results.")

        # 4. Certifications
        certs = parsed_data.get("certifications", [])
        if certs:
            strengths.append(f"Professional certifications present ({', '.join(certs[:3])}).")
        else:
            weaknesses.append("No professional certifications or specialized credentials listed.")
            suggestions.append("Consider earning cloud or framework certifications (e.g. AWS, Scrum Master, Meta Developer) to boost credibility.")

        # 5. Content & Action Verbs
        action_verb_score = ats_results.get("categories", {}).get("action_verbs", {}).get("score", 0)
        if action_verb_score >= 10:
            strengths.append("Good usage of impactful action verbs (built, engineered, optimized).")
        else:
            weaknesses.append("Low density of strong action verbs describing accomplishments.")
            suggestions.append("Begin bullet points with dynamic action verbs like 'Engineered', 'Architected', 'Accelerated', or 'Reduced'.")

        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions
        }
