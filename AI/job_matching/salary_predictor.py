class SalaryPredictor:
    """Estimates market compensation range based on candidate skills, experience level, and location."""

    def predict_salary_range(self, skills: list, experience_years: int = 2, location: str = "US / Remote") -> dict:
        """Computes expected minimum, median, and maximum annual salary in USD."""
        base_min = 80000 + (experience_years * 10000)
        base_med = 110000 + (experience_years * 12000)
        base_max = 140000 + (experience_years * 15000)

        if skills and any(s.lower() in ["docker", "kubernetes", "deep learning", "aws"] for s in skills):
            base_min += 10000
            base_med += 15000
            base_max += 20000

        return {
            "currency": "USD",
            "min_salary": base_min,
            "median_salary": base_med,
            "max_salary": base_max,
            "experience_years": experience_years,
            "location": location,
            "formatted": f"${base_min:,} - ${base_max:,} USD/year"
        }
