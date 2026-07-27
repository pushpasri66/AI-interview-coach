class AmazonInterviewModel:
    """Amazon specific interview pattern, leadership principles, and system design FAQs."""

    COMPANY_NAME = "Amazon"
    LEADERSHIP_PRINCIPLES = ["Customer Obsession", "Ownership", "Bias for Action", "Deep Dive"]

    FAQS = [
        "Describe a time you demonstrated 'Customer Obsession' under tight deadlines.",
        "Design Amazon flash sale checkout handling 100,000 requests per second.",
        "How do you resolve architectural trade-offs when scaling DynamoDB?"
    ]

    def get_company_pattern(self) -> dict:
        return {
            "company": self.COMPANY_NAME,
            "leadership_principles": self.LEADERSHIP_PRINCIPLES,
            "faqs": self.FAQS
        }
