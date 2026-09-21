"""Leaderboard: sum of points (game/series predictions + bracket) per
player, across all engines (points are already computed with the engine
chosen at the time of scripts.run_scoring / scripts.score_bracket)."""
from sqlalchemy import func

from app.auth import login_required
from app.extensions import db
from app.models import BracketPrediction, Player, Prediction
from flask import Blueprint, render_template

bp = Blueprint("leaderboard", __name__)


def compute_standings():
    pred_totals = dict(
        db.session.query(Prediction.player_id, func.coalesce(func.sum(Prediction.points_earned), 0))
        .group_by(Prediction.player_id)
        .all()
    )
    bracket_totals = dict(
        db.session.query(
            BracketPrediction.player_id, func.coalesce(func.sum(BracketPrediction.points_earned), 0)
        )
        .group_by(BracketPrediction.player_id)
        .all()
    )

    rows = []
    for player in Player.query.all():
        total = float(pred_totals.get(player.id) or 0) + float(bracket_totals.get(player.id) or 0)
        rows.append({"player": player, "total": total})

    rows.sort(key=lambda r: r["total"], reverse=True)
    return rows


@bp.route("/classement")
@login_required
def index():
    return render_template("leaderboard.html", rows=compute_standings())
