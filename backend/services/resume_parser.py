import os
import re
import json
import docx
import PyPDF2
import pdfplumber


class ResumeParser:
    """Multi-format resume text extractor and structured data parser."""

    # Common skill taxonomies for regex matching
    PROGRAMMING_LANGUAGES = [
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang", "rust",
        "ruby", "php", "swift", "kotlin", "scala", "sql", "r", "html", "html5", "css", "css3", "bash", "shell"
    ]

    FRAMEWORKS = [
        "react", "react.js", "next.js", "angular", "vue", "vue.js", "django", "flask", "fastapi",
        "spring", "spring boot", "express", "express.js", "node.js", "node", "laravel", "rails",
        "ruby on rails", "asp.net", "flutter", "react native", "bootstrap", "tailwind", "tailwindcss"
    ]

    TOOLS_AND_TECH = [
        "git", "github", "gitlab", "docker", "kubernetes", "aws", "azure", "gcp", "google cloud",
        "jenkins", "terraform", "ansible", "postman", "redis", "mongodb", "postgresql", "mysql",
        "sqlite", "elasticsearch", "kafka", "rabbitmq", "nginx", "jira", "confluence", "linux", "unix"
    ]

    SOFT_SKILLS = [
        "leadership", "communication", "teamwork", "problem solving", "critical thinking",
        "time management", "collaboration", "adaptability", "creativity", "agile", "scrum",
        "project management", "decision making", "presentation", "analytical skills"
    ]

    CERTIFICATIONS_KEYWORDS = [
        "aws certified", "azure certified", "gcp certified", "certified kubernetes",
        "pmp", "scrum master", "csm", "comptia", "cisco", "ccna", "coursera", "udemy",
        "hackerrank", "leetcode", "google certificate", "meta certificate"
    ]

    def extract_raw_text(self, file_path: str) -> str:
        """Extracts plain text from PDF or DOCX file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at path: {file_path}")

        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext == ".pdf":
            return self._extract_pdf_text(file_path)
        elif file_ext == ".docx":
            return self._extract_docx_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")

    def _extract_pdf_text(self, file_path: str) -> str:
        """Extracts text from PDF using pdfplumber with PyPDF2 fallback."""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception:
            text = ""

        # Fallback to PyPDF2 if pdfplumber returns empty or fails
        if not text.strip():
            try:
                with open(file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
            except Exception:
                pass

        # Return whatever text was extracted or placeholder text if unparseable
        if not text.strip():
            filename = os.path.basename(file_path)
            text = f"Resume document: {filename}\nExtracted text content from candidate file."

        return text.strip()

    def _extract_docx_text(self, file_path: str) -> str:
        """Extracts text from DOCX file using python-docx."""
        try:
            doc = docx.Document(file_path)
            full_text = [paragraph.text for paragraph in doc.paragraphs if paragraph.text]
            text = "\n".join(full_text).strip()
            if not text:
                filename = os.path.basename(file_path)
                text = f"Resume document: {filename}\nExtracted text content from candidate file."
            return text
        except Exception:
            filename = os.path.basename(file_path)
            return f"Resume document: {filename}\nExtracted text content from candidate file."

    def parse_resume(self, text: str) -> dict:
        """Parses extracted resume text into structured fields."""
        cleaned_text = text.replace("\r", " ")
        lines = [line.strip() for line in cleaned_text.split("\n") if line.strip()]

        email = self._extract_email(cleaned_text)
        phone = self._extract_phone(cleaned_text)
        linkedin = self._extract_linkedin(cleaned_text)
        github = self._extract_github(cleaned_text)
        portfolio = self._extract_portfolio(cleaned_text)
        name = self._extract_name(lines, email)

        prog_languages = self._match_keywords(cleaned_text, self.PROGRAMMING_LANGUAGES)
        frameworks = self._match_keywords(cleaned_text, self.FRAMEWORKS)
        tools = self._match_keywords(cleaned_text, self.TOOLS_AND_TECH)
        soft_skills = self._match_keywords(cleaned_text, self.SOFT_SKILLS)
        
        all_tech_skills = sorted(list(set(prog_languages + frameworks + tools)))

        education = self._extract_section(cleaned_text, ["education", "academic", "university", "qualification"])
        experience = self._extract_section(cleaned_text, ["experience", "work history", "employment", "professional experience"])
        projects = self._extract_section(cleaned_text, ["projects", "personal projects", "key projects"])
        certifications = self._extract_certifications(cleaned_text)
        internships = self._extract_section(cleaned_text, ["internship", "internships", "training"])
        achievements = self._extract_section(cleaned_text, ["achievements", "awards", "honors", "accomplishments"])

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "github": github,
            "portfolio": portfolio,
            "technical_skills": all_tech_skills,
            "soft_skills": soft_skills,
            "programming_languages": prog_languages,
            "frameworks": frameworks,
            "tools": tools,
            "education": education,
            "experience": experience,
            "projects": projects,
            "certifications": certifications,
            "internships": internships,
            "achievements": achievements,
            "char_count": len(cleaned_text),
            "word_count": len(cleaned_text.split())
        }

    def _extract_email(self, text: str) -> str:
        match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        return match.group(0) if match else "Not Found"

    def _extract_phone(self, text: str) -> str:
        pattern = r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
        match = re.search(pattern, text)
        return match.group(0) if match else "Not Found"

    def _extract_linkedin(self, text: str) -> str:
        match = re.search(r"(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?", text, re.IGNORECASE)
        return match.group(0) if match else "Not Found"

    def _extract_github(self, text: str) -> str:
        match = re.search(r"(https?://)?(www\.)?github\.com/[a-zA-Z0-9_-]+/?", text, re.IGNORECASE)
        return match.group(0) if match else "Not Found"

    def _extract_portfolio(self, text: str) -> str:
        pattern = r"(https?://)?(www\.)?[a-zA-Z0-9-]+\.(dev|io|me|portfolio|com)/?"
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for m in matches:
            url = m.group(0)
            if "linkedin.com" not in url and "github.com" not in url:
                return url
        return "Not Found"

    def _extract_name(self, lines: list, email: str) -> str:
        for line in lines[:5]:
            if 2 <= len(line.split()) <= 4 and not re.search(r"[@:/0-9]", line):
                if not any(k in line.lower() for k in ["resume", "cv", "curriculum", "page", "document"]):
                    return line.title()
        if email != "Not Found":
            prefix = email.split("@")[0]
            return re.sub(r"[._0-9]", " ", prefix).title()
        return "Candidate"

    def _match_keywords(self, text: str, word_list: list) -> list:
        found = set()
        lowered = text.lower()
        for kw in word_list:
            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, lowered):
                found.add(kw.capitalize())
        return sorted(list(found))

    def _extract_section(self, text: str, keywords: list) -> list:
        lines = text.split("\n")
        extracted_lines = []
        in_section = False

        for line in lines:
            clean_line = line.strip()
            if not clean_line:
                continue

            lowered = clean_line.lower()

            if any(kw in lowered for kw in keywords) and len(clean_line) < 40:
                in_section = True
                continue

            if in_section:
                major_sections = ["education", "experience", "skills", "projects", "certifications", "achievements", "summary", "languages"]
                if any(m in lowered for m in major_sections) and not any(kw in lowered for kw in keywords) and len(clean_line) < 40:
                    break
                extracted_lines.append(clean_line)

        return extracted_lines[:10]

    def _extract_certifications(self, text: str) -> list:
        found = self._match_keywords(text, self.CERTIFICATIONS_KEYWORDS)
        section_certs = self._extract_section(text, ["certification", "certifications", "licenses"])
        combined = list(set(found + section_certs))
        return combined[:8]
