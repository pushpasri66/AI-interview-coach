import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logger(app):
    """Configures application-wide logging to logs/app.log."""
    logs_dir = os.path.join(app.root_path, "..", "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir, exist_ok=True)

    log_file = os.path.join(logs_dir, "app.log")

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]: %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Attach handler to app logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("AI Interview Coach logger initialized successfully.")
