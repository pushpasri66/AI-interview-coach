from typing import Dict, Any, List


class OutcomePredictor:
    """Predicts quantitative deltas for career readiness, job match, salary potential, and skill scores."""

    SALARY_BENCHMARKS = {
        "Software Engineer": {"base_min": 85000, "base_max": 115000, "top_min": 120000, "top_max": 155000},
        "AI Engineer": {"base_min": 105000, "base_max": 135000, "top_min": 145000, "top_max": 185000},
        "Machine Learning Engineer": {"base_min": 100000, "base_max": 130000, "top_min": 140000, "top_max": 180000},
        "Full Stack Developer": {"base_min": 80000, "base_max": 110000, "top_min": 115000, "top_max": 145000},
        "Cloud Engineer": {"base_min": 95000, "base_max": 125000, "top_min": 135000, "top_max": 170000},
        "DevOps Engineer": {"base_min": 95000, "base_max": 125000, "top_min": 130000, "top_max": 165000},
        "Data Scientist": {"base_min": 90000, "base_max": 120000, "top_min": 130000, "top_max": 165000},
        "Cybersecurity Engineer": {"base_min": 95000, "base_max": 125000, "top_min": 135000, "top_max": 170000}
    }

    def predict_outcome(
        self,
        scenario_type: str,
        scenario_title: str,
        target_role: str,
        base_readiness: int,
        base_job_match: int,
        base_interview_readiness: int
    ) -> Dict[str, Any]:
        """Calculates multi-dimensional outcome metrics based on scenario type."""
        # 1. Delta Calculations based on scenario type
        if scenario_type == "learn_skill":
            readiness_delta = 8
            job_match_delta = 11
            interview_delta = 5
            salary_growth_pct = 12
            rec_step = "Build a practical proof-of-concept project applying these new skills to solidify your portfolio."
        elif scenario_type == "certification":
            readiness_delta = 10
            job_match_delta = 14
            interview_delta = 7
            salary_growth_pct = 15
            rec_step = "Add this verified certification badge to your LinkedIn and resume headers to increase recruiter search visibility."
        elif scenario_type == "build_project":
            readiness_delta = 12
            job_match_delta = 16
            interview_delta = 9
            salary_growth_pct = 18
            rec_step = "Deploy the project live with CI/CD and record a 2-minute architectural demo walkthrough."
        elif scenario_type == "improve_interview":
            readiness_delta = 9
            job_match_delta = 12
            interview_delta = 18
            salary_growth_pct = 16
            rec_step = "Schedule an AI Mock Interview focusing on your weakest category to validate score gains."
        elif scenario_type == "change_role":
            readiness_delta = 6
            job_match_delta = 9
            interview_delta = 6
            salary_growth_pct = 14
            rec_step = f"Follow the 3-phase transition roadmap for {target_role} starting with core skill bridge milestones."
        elif scenario_type == "apply_jobs":
            readiness_delta = 4
            job_match_delta = 7
            interview_delta = 5
            salary_growth_pct = 10
            rec_step = "Use the AI Job Application Assistant to generate tailored cover letters and resume keywords before submitting."
        else:
            readiness_delta = 7
            job_match_delta = 9
            interview_delta = 6
            salary_growth_pct = 11
            rec_step = "Continue structured daily career planning practice."

        pred_readiness = min(98, base_readiness + readiness_delta)
        pred_job_match = min(98, base_job_match + job_match_delta)
        pred_interview = min(98, base_interview_readiness + interview_delta)

        # 2. Salary Potential Modeling
        role_bench = self.SALARY_BENCHMARKS.get(target_role, self.SALARY_BENCHMARKS["Software Engineer"])
        cur_min = role_bench["base_min"]
        cur_max = role_bench["base_max"]
        
        pred_min = int(cur_min * (1 + salary_growth_pct / 100))
        pred_max = int(cur_max * (1 + salary_growth_pct / 100))

        cur_salary_str = f"${cur_min:,} - ${cur_max:,}"
        pred_salary_str = f"${pred_min:,} - ${pred_max:,}"

        return {
            "current_readiness": base_readiness,
            "predicted_readiness": pred_readiness,
            "readiness_delta": pred_readiness - base_readiness,
            "current_job_match": base_job_match,
            "predicted_job_match": pred_job_match,
            "job_match_delta": pred_job_match - base_job_match,
            "current_interview_readiness": base_interview_readiness,
            "predicted_interview_readiness": pred_interview,
            "current_salary_est": cur_salary_str,
            "predicted_salary_est": pred_salary_str,
            "salary_growth_pct": salary_growth_pct,
            "recommended_next_step": rec_step
        }
