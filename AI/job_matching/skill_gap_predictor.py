class SkillGapPredictor:
    """Predicts missing tech stack requirements for target job roles."""

    def predict_missing_skills(self, candidate_skills: list, target_role: str = "AI Engineer") -> dict:
        """Computes matched vs missing skill gap matrix."""
        cand_clean = [s.lower().strip() for s in candidate_skills] if candidate_skills else ["python", "machine learning"]
        role_reqs = ["python", "machine learning", "flask", "docker", "kubernetes", "aws", "postgresql"]

        matched = [r.title() for r in role_reqs if any(r in cs or cs in r for cs in cand_clean)]
        missing = [r.title() for r in role_reqs if r.title() not in matched]

        return {
            "target_role": target_role,
            "matched_skills": matched,
            "missing_skills": missing,
            "gap_percentage": int((len(missing) / len(role_reqs)) * 100)
        }
