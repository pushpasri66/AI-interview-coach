# ☁️ AI Interview Coach - Cloud Deployment Guide

Comprehensive instructions for deploying **AI Interview Coach** to AWS, Microsoft Azure, and Render/Railway.

---

## 1. Deploying to AWS (Amazon Web Services)

### Architecture
- **EC2 Instance (Ubuntu 24.04 LTS)**: Runs Nginx & Gunicorn web application.
- **RDS (PostgreSQL)**: Managed relational database.
- **S3 Bucket**: Stores uploaded resumes, audio files, video frames, and PDF reports.
- **ElastiCache (Redis)**: Rate limiting and session caching.

### Step-by-Step AWS Setup
1. **Launch RDS PostgreSQL Instance**:
   - Engine: PostgreSQL 16.
   - DB Name: `ai_interview_coach`.
   - Record endpoint host address and master credentials.
2. **Launch EC2 Instance**:
   - Instance Type: `t3.medium` or higher.
   - Security Group: Allow TCP 80, 443, 22.
3. **Deploy with Docker Compose**:
   ```bash
   git clone https://github.com/your-org/AI-Interview-Coach.git
   cd AI-Interview-Coach
   cp .env.example .env
   # Update DATABASE_URL with RDS endpoint
   docker-compose -f deployment/docker-compose.yml up -d --build
   ```

---

## 2. Deploying to Microsoft Azure

### Architecture
- **Azure App Service (Linux)**: Hosts Python 3.14 web container.
- **Azure Database for PostgreSQL**: Managed database.
- **Azure Blob Storage**: Media storage.

### Step-by-Step Azure Setup
1. **Create PostgreSQL Flexible Server**:
   ```bash
   az postgres flexible-server create --resource-group ai-coach-rg --name aicoach-db-server --admin-user postgres --admin-password YourPassword123!
   ```
2. **Deploy App Service**:
   ```bash
   az webapp up --name ai-interview-coach-app --resource-group ai-coach-rg --runtime "PYTHON:3.14"
   ```

---

## 3. Deploying to Render / Railway

### Render Deployment
1. Connect GitHub repository to **Render.com**.
2. Create **PostgreSQL Database** on Render.
3. Create **Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -c deployment/gunicorn.conf.py app:app`
4. Set Environment Variables (`DATABASE_URL`, `SECRET_KEY`, `FLASK_ENV=production`).
