class JobMatchEngine:
    """Real Job Matching Engine comparing candidate profiles against live job requirements."""

    def match_candidate_to_job(self, candidate_skills: list, job_requirements: list, target_role: str = "AI Engineer") -> dict:
        """Computes job compatibility match score and missing stack."""
        cand_clean = [s.lower().strip() for s in candidate_skills] if candidate_skills else ["python", "machine learning", "flask"]
        req_clean = [r.lower().strip() for r in job_requirements] if job_requirements else ["python", "machine learning", "flask", "aws", "docker", "kubernetes"]

        matched = [r.title() for r in req_clean if any(r in cs or cs in r for cs in cand_clean)]
        missing = [r.title() for r in req_clean if r.title() not in matched]

        match_pct = int((len(matched) / max(1, len(req_clean))) * 100)

        return {
            "target_role": target_role,
            "match_percentage": match_pct,
            "matched_skills": matched,
            "missing_skills": missing,
            "summary": f"Role: {target_role} | Match: {match_pct}% | Matched: {', '.join(matched[:3])} | Missing: {', '.join(missing[:3])}"
        }
