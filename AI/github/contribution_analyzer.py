from typing import Dict, Any, List


class ContributionAnalyzer:
    """Analyzes commit frequency, repository update recency, stars, forks, and open-source contribution."""

    def evaluate_activity_and_contributions(
        self,
        public_repos_count: int,
        total_stars: int,
        total_forks: int,
        recent_updates_count: int
    ) -> Dict[str, Any]:
        """Calculates coding activity score and open-source impact."""
        # 1. Coding Activity Score (0-100)
        activity_score = 45
        activity_score += min(25, public_repos_count * 3)
        activity_score += min(20, recent_updates_count * 5)
        if total_stars > 5 or total_forks > 2:
            activity_score += 10
        activity_score = min(100, max(30, activity_score))

        # 2. Activity Level Descriptor
        if activity_score >= 85:
            activity_level = "Very High (Daily/Weekly Committer)"
        elif activity_score >= 70:
            activity_level = "Consistent & Active"
        elif activity_score >= 50:
            activity_level = "Moderate Contribution Cadence"
        else:
            activity_level = "Sporadic / Occasional"

        # 3. Open Source Contribution Score (0-100)
        os_score = 40
        os_score += min(25, total_stars * 4)
        os_score += min(20, total_forks * 5)
        os_score += min(15, public_repos_count * 2)
        os_score = min(100, max(25, os_score))

        return {
            "coding_activity_score": activity_score,
            "commit_activity_level": activity_level,
            "opensource_contribution_score": os_score,
            "total_stars": total_stars,
            "total_forks": total_forks,
            "active_repos_ratio": f"{min(recent_updates_count, public_repos_count)}/{max(1, public_repos_count)}"
        }
