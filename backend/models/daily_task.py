import json
from datetime import datetime
from backend.database import db


class DailyPlan(db.Model):
    """Database model storing candidate personalized daily career development tasks, completion status, and progress."""

    __tablename__ = "daily_plans"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_date = db.Column(db.String(20), nullable=False, index=True)  # YYYY-MM-DD
    
    total_estimated_minutes = db.Column(db.Integer, default=0, nullable=False)
    completed_minutes = db.Column(db.Integer, default=0, nullable=False)
    completion_rate = db.Column(db.Integer, default=0, nullable=False)  # 0-100%
    
    tasks_json = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def get_tasks(self) -> list:
        return json.loads(self.tasks_json) if self.tasks_json else []

    def set_tasks(self, data: list) -> None:
        self.tasks_json = json.dumps(data)
        self.recalculate_progress()

    def recalculate_progress(self) -> None:
        tasks = self.get_tasks()
        if not tasks:
            self.total_estimated_minutes = 0
            self.completed_minutes = 0
            self.completion_rate = 0
            return

        total_mins = sum(t.get("duration_minutes", 15) for t in tasks)
        done_mins = sum(t.get("duration_minutes", 15) for t in tasks if t.get("completed", False))
        done_count = sum(1 for t in tasks if t.get("completed", False))

        self.total_estimated_minutes = total_mins
        self.completed_minutes = done_mins
        self.completion_rate = int((done_count / len(tasks)) * 100) if tasks else 0

    def mark_task_status(self, task_id: str, completed: bool = True) -> bool:
        """Finds task by string ID or index and updates completed flag."""
        tasks = self.get_tasks()
        found = False
        for t in tasks:
            if str(t.get("id")) == str(task_id) or str(t.get("task_id")) == str(task_id):
                t["completed"] = completed
                t["completed_at"] = datetime.utcnow().isoformat() if completed else None
                found = True
                break

        if not found and task_id.isdigit():
            idx = int(task_id)
            if 0 <= idx < len(tasks):
                tasks[idx]["completed"] = completed
                tasks[idx]["completed_at"] = datetime.utcnow().isoformat() if completed else None
                found = True

        if found:
            self.set_tasks(tasks)
        return found

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "plan_date": self.plan_date,
            "metrics": {
                "total_estimated_minutes": self.total_estimated_minutes,
                "completed_minutes": self.completed_minutes,
                "completion_rate": self.completion_rate,
                "total_tasks": len(self.get_tasks()),
                "completed_tasks": sum(1 for t in self.get_tasks() if t.get("completed", False))
            },
            "tasks": self.get_tasks(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f"<DailyPlan id={self.id} user_id={self.user_id} date='{self.plan_date}' rate={self.completion_rate}%>"
