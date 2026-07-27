class MicrosoftInterviewModel:
    """Microsoft specific interview pattern and Azure cloud architecture FAQs."""

    COMPANY_NAME = "Microsoft"

    FAQS = [
        "How does Azure Blob Storage ensure high availability and disaster recovery?",
        "Explain OOP principles in C# / C++ / Java and runtime polymorphism.",
        "Design a cloud-based collaborative document editing platform."
    ]

    def get_company_pattern(self) -> dict:
        return {
            "company": self.COMPANY_NAME,
            "faqs": self.FAQS
        }
