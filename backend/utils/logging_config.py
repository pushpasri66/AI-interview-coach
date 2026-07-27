import os
import logging
from logging.handlers import RotatingFileHandler


def setup_advanced_logging(app):
    """Sets up multi-channel rotating loggers for app, errors, security, AI engine, and access logs."""
    logs_dir = os.path.abspath(os.path.join(app.root_path, "..", "logs"))
    os.makedirs(logs_dir, exist_ok=True)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    # 1. Main App Logger (app.log)
    app_handler = RotatingFileHandler(
        os.path.join(logs_dir, "app.log"), maxBytes=5 * 1024 * 1024, backupCount=5
    )
    app_handler.setFormatter(formatter)
    app_handler.setLevel(logging.INFO)

    # 2. Error Logger (error.log)
    error_handler = RotatingFileHandler(
        os.path.join(logs_dir, "error.log"), maxBytes=5 * 1024 * 1024, backupCount=5
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)

    # 3. Security Logger (security.log)
    sec_logger = logging.getLogger("security")
    sec_handler = RotatingFileHandler(
        os.path.join(logs_dir, "security.log"), maxBytes=5 * 1024 * 1024, backupCount=5
    )
    sec_handler.setFormatter(formatter)
    sec_logger.addHandler(sec_handler)
    sec_logger.setLevel(logging.INFO)

    # 4. AI Engine Logger (ai_engine.log)
    ai_logger = logging.getLogger("ai_engine")
    ai_handler = RotatingFileHandler(
        os.path.join(logs_dir, "ai_engine.log"), maxBytes=5 * 1024 * 1024, backupCount=5
    )
    ai_handler.setFormatter(formatter)
    ai_logger.addHandler(ai_handler)
    ai_logger.setLevel(logging.INFO)

    # Attach handlers to Flask app
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(app_handler)
    app.logger.addHandler(error_handler)

    app.logger.info("Advanced multi-channel logging system initialized successfully.")
