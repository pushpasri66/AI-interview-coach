import time
import os
from datetime import datetime
from backend.database import db


class MonitoringService:
    """Service providing real-time application health checks, database status, and API metrics."""

    def get_system_health(self) -> dict:
        """Returns application health status metrics."""
        db_healthy = True
        try:
            db.session.execute(db.select(1)).first()
        except Exception:
            db_healthy = False

        return {
            "status": "Healthy" if db_healthy else "Degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "database_connected": db_healthy,
            "environment": os.getenv("FLASK_ENV", "development"),
            "uptime_status": "Running smoothly"
        }
