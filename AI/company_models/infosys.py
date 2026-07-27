class InfosysInterviewModel:
    """Infosys specific interview pattern, technical fundamentals, and problem solving FAQs."""

    COMPANY_NAME = "Infosys"

    FAQS = [
        "Explain the difference between primary key, unique key, and foreign key.",
        "How do you implement binary search and what is its time complexity?",
        "Explain REST API principles and HTTP status codes (200, 400, 404, 500)."
    ]

    def get_company_pattern(self) -> dict:
        return {
            "company": self.COMPANY_NAME,
            "faqs": self.FAQS
        }
