class TCSInterviewModel:
    """TCS specific interview pattern, software engineering process, and technical FAQs."""

    COMPANY_NAME = "TCS"

    FAQS = [
        "Explain SDLC phases, Agile methodologies, and release deliverables.",
        "What is normalization in DBMS and how do 1NF, 2NF, and 3NF differ?",
        "Explain OOP principles and exception handling in Java / C++."
    ]

    def get_company_pattern(self) -> dict:
        return {
            "company": self.COMPANY_NAME,
            "faqs": self.FAQS
        }
