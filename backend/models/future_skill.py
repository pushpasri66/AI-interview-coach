import json
from datetime import datetime
from backend.database import db


class FutureSkillDemand(db.Model):
    """Database model for future industry skill demand predictions (1-year, 2-year, 3-year outlooks)."""

    __tablename__ = "future_skill_demands"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    
    # Demand index ratings (0-100)
    current_demand = db.Column(db.Integer, default=70, nullable=False)
    demand_1yr = db.Column(db.Integer, default=75, nullable=False)
    demand_2yr = db.Column(db.Integer, default=82, nullable=False)
    demand_3yr = db.Column(db.Integer, default=90, nullable=False)
    
    # Growth and priority metrics
    growth_percentage = db.Column(db.Float, default=15.0, nullable=False)
    importance = db.Column(db.String(50), default="High", nullable=False)  # "Critical", "High", "Medium"
    learning_priority = db.Column(db.String(50), default="Immediate", nullable=False)  # "Immediate", "Medium-term", "Long-term"
    market_drivers = db.Column(db.Text, nullable=True)  # Key reasons driving demand
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "skill_name": self.skill_name,
            "category": self.category,
            "current_demand": self.current_demand,
            "demand_forecast": {
                "1_year": self.demand_1yr,
                "2_year": self.demand_2yr,
                "3_year": self.demand_3yr
            },
            "growth_percentage": round(self.growth_percentage, 1),
            "importance": self.importance,
            "learning_priority": self.learning_priority,
            "market_drivers": self.market_drivers.split(";") if self.market_drivers else []
        }

    def __repr__(self) -> str:
        return f"<FutureSkillDemand id={self.id} skill='{self.skill_name}' growth={self.growth_percentage}%>"
