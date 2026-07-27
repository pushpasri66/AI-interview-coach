import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory Path
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")


class Config:
    """Base application configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "prod-secret-key-ai-interview-coach-2026-xyz!")
    
    # SQLite default for development with POSIX path normalization
    DB_DIR = BASE_DIR / "database"
    os.makedirs(DB_DIR, exist_ok=True)
    DEFAULT_DB_PATH = (DB_DIR / "interview.db").as_posix()
    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Upload & Media Configuration
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", (BASE_DIR / "uploads").as_posix())
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))  # 16 MB limit
    ALLOWED_EXTENSIONS = {"pdf", "docx", "png", "jpg", "jpeg", "wav", "mp3", "mp4", "webm", "ogg"}

    # Mail Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")

    # AI API Keys
    AI_API_KEY = os.getenv("AI_API_KEY", "default-ai-coach-api-key")

    # Rate Limiter
    RATELIMIT_DEFAULT = "200 per day; 50 per hour"
    RATELIMIT_STORAGE_URI = os.getenv("REDIS_URL", "memory://")

    # Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    REMOTE_ADDR_HEADER = "X-Forwarded-For"


class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
