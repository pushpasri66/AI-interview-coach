# 🚀 AI Interview Coach – Complete AI Career Ecosystem & Autonomous Intelligence Platform

**AI Interview Coach** is an enterprise-grade, full-stack AI career intelligence, mock interview simulation, and career twin platform designed for students, engineering professionals, recruiters, and career development organizations.

---

## 🏛️ System Architecture Overview (Phases 1 – 9)

```
AI Interview Coach Architecture
├── 1️⃣ Core Infrastructure & Auth (Phase 1)
│   └── Flask, SQLAlchemy, Flask-Login, Scrypt Password Hashing, CSRF Security
│
├── 2️⃣ AI Resume Analyzer & ATS Engine (Phase 2)
│   └── PDF/DOCX Parser, 100-Point ATS Scorer, ReportLab PDF Performance Reports
│
├── 3️⃣ AI Mock Interview Platform (Phase 3)
│   └── HR, Technical Domain, Coding Sandbox, Target Company Mock Interviews
│
├── 4️⃣ Advanced AI Multimodal Analysis (Phase 4)
│   └── Computer Vision Emotion Tracking, Eye Contact, Voice Pitch & Cadence
│
├── 5️⃣ AI Analytics & Career Recommendations (Phase 5)
│   └── Career Role Predictor, Skill Gap Analyzer, 4-Month Roadmaps, Chart.js
│
├── 6️⃣ Production Cloud & Security Hardening (Phase 6)
│   └── Flask-Limiter, Multi-Channel Logging, PostgreSQL/SQLite, Gunicorn, Docker Compose, CI/CD
│
├── 7️⃣ LLM Conversational & Avatar Engine (Phase 7)
│   └── LLM Follow-Up Interviewer, AI Avatar Lip Sync, Multi-Language, PyJWT Mobile API
│
├── 8️⃣ AI Career Ecosystem & Enterprise Intelligence (Phase 8)
│   ├── AI Career Mentor System (`AI/mentor/`)
│   ├── AI Job Recommendation Engine (`AI/job_matching/`)
│   ├── AI Resume Builder & Optimizer 2.0 (`backend/services/resume_builder.py`)
│   ├── AI LinkedIn Profile Analyzer (`AI/linkedin/`)
│   ├── Real-Time Interview Intelligence 2.0 (`AI/realtime/`)
│   ├── AI Mock Group Discussion Platform (`backend/routes/group_discussion.py`)
│   ├── Recruiter & Company Portal (`backend/routes/recruiter.py`)
│   ├── AI Coding Interview Platform 2.0 (`AI/code_review/`)
│   ├── Multilingual Voice AI Assistant (`AI/voice_assistant/`)
│   └── Blockchain-Style Certificate Verification (`backend/services/certificate.py`)
│
└── 9️⃣ Autonomous Career Intelligence & Digital Twin (Phase 9)
    ├── 🧬 AI Career Digital Twin (`AI/digital_twin/`, `backend/models/digital_twin.py`)
    ├── 🔮 Predictive Career Path Intelligence (`AI/career_prediction/`, `backend/models/career_prediction.py`)
    ├── 📈 Future Skill Intelligence Engine (`AI/future_skills/`, `backend/models/future_skill.py`)
    ├── 🎯 AI Interview Question Prediction Engine (`AI/question_prediction/`, `backend/models/question_prediction.py`)
    ├── 🐙 GitHub AI Profile Analyzer (`AI/github/`, `backend/models/github_profile.py`)
    ├── 📝 AI Job Application Assistant (`AI/job_application/`, `backend/models/job_application.py`)
    ├── 💡 Explainable AI & Score Diagnostics (`AI/explainable/`)
    ├── 📅 Personalized Daily Career Planner (`AI/daily_planner/`, `backend/models/daily_task.py`)
    ├── 🧪 AI Career Simulation Engine (`AI/simulator/`, `backend/models/career_simulation.py`)
    ├── 📊 Advanced AI Career Intelligence Dashboard (`frontend/templates/career_intelligence.html`)
    └── 📄 AI Career Intelligence PDF Reports (`backend/services/career_report.py`)
```

---

## 🧠 Phase 9 Deep-Dive: Autonomous Career Intelligence Modules

### 1. AI Career Digital Twin (`AI/digital_twin/`)
- Dynamic multi-pillar candidate state engine integrating resumes, verified skills, mock interviews, coding tests, and career milestones.
- Real-time calculations for **Career Readiness Index**, **Technical Strength**, **Communication Score**, and **Target Role Match**.
- Automatic event-driven recalibration triggered upon interview completion, test execution, or daily plan check-offs.

### 2. Predictive Career Path Intelligence (`AI/career_prediction/`)
- Evaluates fit against 9 major industry roles:
  - *AI Engineer*, *Machine Learning Engineer*, *Data Scientist*, *Data Analyst*, *Software Engineer*, *Full Stack Developer*, *Cloud Engineer*, *DevOps Engineer*, *Cybersecurity Engineer*.
- For each role: calculates match %, existing vs. missing skills, recommended certifications, and preparation timelines.

### 3. Future Skill Demand Intelligence (`AI/future_skills/`)
- Predictive 1-year, 2-year, and 3-year market demand curves for emerging technologies (e.g. *RAG*, *Autonomous Agents*, *MLOps*, *Kubernetes*, *Zero-Trust Security*).
- Projects demand growth percentages and flags high-priority learning objectives.

### 4. AI Interview Question Prediction Engine (`AI/question_prediction/`)
- Analyzes candidate background against target company and job descriptions.
- Generates high-probability questions across 7 categories: `HR`, `Technical`, `Coding`, `System Design`, `Project`, `Behavioral`, and `Company-specific` with explainable prediction rationale.

### 5. GitHub AI Profile Analyzer (`AI/github/`)
- Comprehensive repository and commit activity evaluation.
- Calculates 10 core metrics: *Coding Activity*, *Repository Quality*, *Language Distribution*, *Commit Cadence*, *Project Complexity*, *README Quality*, *Documentation Quality*, *Project Diversity*, *Open-Source Contributions*, and *Composite GitHub Score*.

### 6. AI Job Application Assistant (`AI/job_application/`)
- Tailors candidate resumes to target job descriptions, computes ATS keyword match percentages, generates cover letters, and crafts screening answers.

### 7. Explainable AI (`AI/explainable/`)
- Transparent diagnostic engine explaining positive factors, negative factors, and actionable improvement steps behind all AI scores.

### 8. Personalized Daily Career Planner (`AI/daily_planner/`)
- Generates personalized daily study and practice tasks based on identified skill gaps and interview timelines.
- One-click task completion triggers automatic **Digital Twin** score updates.

### 9. AI Career Simulation Engine (`AI/simulator/`)
- What-If simulation engine allowing candidates to simulate learning a skill, completing a certification, or building a project.
- Projects live deltas: Career Readiness ($+\Delta\%$), Job Match ($+\Delta\%$), and Salary Growth potential.

### 10. Unified Career Intelligence Dashboard (`/career/career-intelligence`)
- Responsive glassmorphic interface with Chart.js line, bar, and gauge visualizations.

### 11. Professional PDF Career Reports (`/api/career/report`)
- Publication-grade ReportLab PDF generation for 4 report types: *Intelligence Dossier*, *Readiness Report*, *Skill Gap Report*, and *Job Application Strategy*.

---

## 🔒 Security & Authorization

- **Dual-Layer Authentication**: Supports Flask-Login session cookies and standard `Authorization: Bearer <JWT>` headers.
- **Tenant & Candidate Isolation**: All API endpoints enforce candidate ID verification; no candidate can access another candidate's reports, simulations, or profiles.
- **Rate Limiting**: Integrated `Flask-Limiter` preventing abuse.
- **CSRF Protection**: Enabled across all state-mutating web forms.
- **Input Sanitization**: File uploads strictly validate MIME types, extensions, and file sizes.

---

## 📡 REST API Reference

| Method | Endpoint | Auth | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/career/digital-twin` | Required | Retrieve candidate Digital Twin state |
| `GET` | `/api/career/paths` | Required | 9-role predictive career path evaluation |
| `GET` | `/api/career/future-skills` | Required | 1/2/3-year future skill forecasts |
| `GET` | `/api/career/skill-gaps` | Required | Candidate target role skill gaps |
| `POST` | `/api/career/interview-predictions` | Required | Generate likely interview questions |
| `GET` | `/api/career/interview-predictions` | Required | Retrieve question prediction history |
| `GET` | `/api/github/analyze` | Required | Analyze GitHub profile metrics |
| `POST` | `/api/career/job-application` | Required | Generate tailored resume & cover letter |
| `GET` | `/api/career/job-application/history` | Required | Retrieve job application history |
| `GET` | `/api/career/daily-plan` | Required | Retrieve daily career plan |
| `POST` | `/api/career/daily-plan/complete` | Required | Complete daily task & sync Digital Twin |
| `POST` | `/api/career/simulate` | Required | Run What-If career simulation |
| `GET` | `/api/career/simulations` | Required | Retrieve simulation history |
| `GET` | `/api/career/report` | Required | Generate and stream/download PDF report |

---

## 🚀 Installation & Quickstart

```bash
# 1. Clone repository & create virtual environment
git clone https://github.com/pushpasri66/AI-interview-coach.git
cd AI-interview-coach
python -m venv venv
.\venv\Scripts\activate   # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run full test discovery
python -m unittest discover tests

# 4. Start Flask server
python run.py
```

Open your browser at: **`http://127.0.0.1:5000`**

---

## 🧪 Testing

```bash
# Run all Phase 1 - 9 test suites
python -m unittest discover tests -v
```
- **Total Test Count**: 126 unit & integration tests across all modules.
- **Pass Rate**: 100% OK.
