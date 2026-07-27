class CompanyMatcher:
    """Matches candidate preferences and technical profile with corporate tech stacks and company cultures."""

    def match_company_culture(self, skills: list, preferred_work_style: str = "Hybrid") -> list:
        """Returns matched companies."""
        return [
            {"company": "Google", "culture_match": 95, "tech_alignment": "High", "work_style": "Hybrid"},
            {"company": "Amazon", "culture_match": 90, "tech_alignment": "High", "work_style": "Remote / Office"},
            {"company": "Microsoft", "culture_match": 88, "tech_alignment": "Medium-High", "work_style": "Hybrid"}
        ]
