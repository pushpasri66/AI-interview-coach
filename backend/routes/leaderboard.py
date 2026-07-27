from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user

from backend.database import db
from backend.models.user import User
from backend.models.gamification import Gamification

leaderboard_bp = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")


@leaderboard_bp.route("/")
@login_required
def index():
    """Renders candidate leaderboard and gamification ranking system."""
    rankings = db.session.query(User, Gamification)\
        .join(Gamification, User.id == Gamification.user_id)\
        .order_by(Gamification.points.desc()).limit(20).all()

    # Format list
    leaderboard_list = []
    user_rank = 1
    user_game_info = None

    for idx, (user_rec, game_rec) in enumerate(rankings, 1):
        if user_rec.id == current_user.id:
            user_rank = idx
            user_game_info = game_rec

        leaderboard_list.append({
            "rank": idx,
            "user_id": user_rec.id,
            "fullname": user_rec.fullname,
            "points": game_rec.points,
            "level": game_rec.level,
            "streak": game_rec.streak,
            "badges": game_rec.get_badges_list()
        })

    if not user_game_info:
        user_game_info = Gamification.query.filter_by(user_id=current_user.id).first()
        if not user_game_info:
            user_game_info = Gamification(user_id=current_user.id, points=150, level=1, streak=3)
            db.session.add(user_game_info)
            db.session.commit()

    return render_template(
        "leaderboard.html",
        leaderboard=leaderboard_list,
        user_rank=user_rank,
        user_game=user_game_info
    )
