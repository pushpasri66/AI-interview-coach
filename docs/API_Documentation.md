# 📚 AI Interview Coach - REST API Documentation

Comprehensive API documentation for authentication, resume analysis, mock interview sessions, multimodal AI feedback, analytics, and career recommendations.

---

## 1. Authentication Endpoints

### POST `/register`
Registers a new candidate account.
* **Request Body (Form / JSON):**
  - `fullname`: string (Required)
  - `email`: string (Required)
  - `password`: string (Required, min 8 chars with uppercase, lowercase, digit, special char)
* **Responses:**
  - `200 OK`: Account created successfully.
  - `400 Bad Request`: Email already registered or invalid password strength.

### POST `/login`
Authenticates candidate credentials and establishes session.
* **Request Body (Form / JSON):**
  - `email`: string
  - `password`: string
* **Rate Limit:** 10 requests / minute.
* **Responses:**
  - `200 OK`: Login successful. Redirects to `/dashboard`.
  - `401 Unauthorized`: Invalid credentials.

### GET/POST `/logout`
Terminates candidate login session.

---

## 2. Resume & ATS Analysis Endpoints

### POST `/resume/upload`
Uploads resume PDF/DOCX file and executes 100-point ATS parser.
* **Request Body:** `multipart/form-data` with `file`
* **File Restrictions:** PDF or DOCX format, max 16 MB.
* **Responses:**
  - `200 OK`: Returns ATS score %, contact info, tech skills, strengths, and suggestions.

### GET `/resume/history`
Renders candidate resume version comparison history.

### GET `/resume/download_report/<analysis_id>`
Downloads ReportLab PDF ATS report.

---

## 3. Mock Interview Engine Endpoints

### POST `/interview/generate`
Generates an interview session with tailored questions.
* **Request Form Data:**
  - `interview_type`: string (`hr`, `technical`, `coding`, `company`, `resume`)
  - `category`: string (`python`, `java`, `ai_ml`, `dsa`, `dbms`, `sql`, `cn`, `os`)
  - `company_name`: string (`Google`, `Microsoft`, `Amazon`, `TCS`, `Infosys`, `Wipro`, `Accenture`)
  - `difficulty`: string (`easy`, `medium`, `hard`)
* **Responses:**
  - `302 Found`: Redirects to `/interview/room/<interview_id>`.

### POST `/interview/answer`
Evaluates candidate response via AI engine.
* **Request JSON:**
  - `interview_id`: integer
  - `question_id`: integer
  - `user_answer`: string
* **Rate Limit:** 30 requests / minute.
* **Responses:**
  - `200 OK`: Returns overall score, technical depth, relevance, communication, feedback notes.

### GET `/interview/result/<interview_id>`
Renders interview report breakdown and PDF download link.

---

## 4. Multimodal AI Analysis Endpoints

### GET `/analysis/live/<interview_id>`
Renders live camera feed room with real-time confidence & emotion meters.

### POST `/analysis/upload_video`
Handles webcam frame/video snapshots for computer vision emotion analysis.

### POST `/analysis/process`
Calculates overall multimodal score (Voice 25% + Confidence 25% + Technical 20% + Emotion 15% + Eye Contact 15%).

---

## 5. Analytics & Career Endpoints

### GET `/analytics/dashboard`
Renders Chart.js analytics dashboard (Line, Bar, Radar, Doughnut charts).

### GET `/analytics/progress`
Returns progress JSON metrics.

### GET `/career/recommendations`
Returns AI matched job roles (ML Engineer, AI Engineer, Data Scientist, Backend Developer).

### POST `/career/analyze-job`
Parses target job description text and computes compatibility match score %.
