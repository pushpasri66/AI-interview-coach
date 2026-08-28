from typing import Dict, Any, List


class ProgressOptimizer:
    """Optimizes candidate study pacing, completion velocity, and daily time budgets."""

    def optimize_daily_schedule(
        self,
        tasks: List[Dict[str, Any]],
        target_daily_budget_minutes: int = 140
    ) -> Dict[str, Any]:
        """Balances daily tasks to match target study time budget and calculates velocity."""
        total_minutes = sum(t.get("duration_minutes", 15) for t in tasks)
        completed_tasks = [t for t in tasks if t.get("completed", False)]
        completed_minutes = sum(t.get("duration_minutes", 15) for t in completed_tasks)

        completion_rate = int((len(completed_tasks) / max(1, len(tasks))) * 100)

        # Calculate momentum rating
        if completion_rate == 100:
            momentum = "Maximum Velocity (All Tasks Done)"
        elif completion_rate >= 50:
            momentum = "Strong Progress"
        elif completion_rate > 0:
            momentum = "In Progress"
        else:
            momentum = "Ready to Start"

        return {
            "total_tasks_count": len(tasks),
            "completed_tasks_count": len(completed_tasks),
            "total_estimated_minutes": total_minutes,
            "completed_minutes": completed_minutes,
            "completion_rate_pct": completion_rate,
            "momentum_rating": momentum,
            "target_daily_budget_minutes": target_daily_budget_minutes
        }
