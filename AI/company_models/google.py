class GoogleInterviewModel:
    """Google specific interview pattern, evaluation bar, and question bank."""

    COMPANY_NAME = "Google"
    EVALUATION_BAR = "High Algorithmic Rigor & System Scalability"

    FAQS = [
        "How would you design a distributed web crawler scaling to 10 billion pages?",
        "Explain Google MapReduce architecture and how data locality optimizes computation.",
        "How would you implement a rate limiter for 1 million requests/sec?"
    ]

    def get_company_pattern(self) -> dict:
        return {
            "company": self.COMPANY_NAME,
            "bar": self.EVALUATION_BAR,
            "faqs": self.FAQS
        }
