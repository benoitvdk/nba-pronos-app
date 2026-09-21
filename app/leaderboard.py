"""Leaderboard: sum of points (game/series predictions + bracket) per
player, across all engines (points are already computed with the engine
chosen at the time of scripts.run_scoring / scripts.score_bracket)."""
from datetime import datetime, timezone

from flask import Blueprint, g, render_template
from sqlalchemy import func

from app.auth import login_required
from app.bracket import CATEGORIES
from app.extensions import db
from app.models import BracketPrediction, Game, Player, Prediction, Series
from app.time_utils import ensure_aware_utc

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


def _bracket_is_locked():
    return db.session.query(Game.query.filter(Game.result.isnot(None)).exists()).scalar()


@bp.route("/classement")
@login_required
def index():
    return render_template("leaderboard.html", rows=compute_standings())


@bp.route("/joueur/<int:player_id>")
@login_required
def player_profile(player_id):
    """Player profile page: every prediction they've made, game by game,
    series by series, and bracket. Same visibility rule as everywhere else
    in the app (see app/home.py): a prediction is only visible to OTHER
    players once its game/series is locked, never before - own profile
    always shows everything."""
    player = db.get_or_404(Player, player_id)
    is_self = g.player.id == player.id
    now = datetime.now(timezone.utc)

    bracket_visible = is_self or _bracket_is_locked()
    bracket_preds = {
        p.category: p for p in BracketPrediction.query.filter_by(player_id=player.id).all()
    }
    bracket_rows = []
    for key, label in CATEGORIES:
        pred = bracket_preds.get(key)
        if pred is None:
            continue
        bracket_rows.append(
            {"label": label, "prediction": pred if bracket_visible else None, "hidden": not bracket_visible}
        )

    series_rows = []
    for series in Series.query.order_by(Series.id).all():
        started = any(gm.result is not None for gm in series.games)
        series_visible = is_self or started

        winner_pred = Prediction.query.filter_by(
            player_id=player.id, prediction_type="series_winner", series_id=series.id
        ).first()
        score_pred = Prediction.query.filter_by(
            player_id=player.id, prediction_type="series_score", series_id=series.id
        ).first()

        games_rows = []
        for game in series.games.order_by(Game.game_date).all():
            game_pred = Prediction.query.filter_by(
                player_id=player.id, prediction_type="game_winner", game_id=game.id
            ).first()
            if game_pred is None:
                continue
            game_open = game.result is None and ensure_aware_utc(game.game_date) > now
            game_visible = is_self or not game_open
            games_rows.append(
                {"game": game, "prediction": game_pred if game_visible else None, "hidden": not game_visible}
            )

        if winner_pred is None and score_pred is None and not games_rows:
            continue

        series_rows.append(
            {
                "series": series,
                "winner_prediction": winner_pred if series_visible else None,
                "winner_hidden": winner_pred is not None and not series_visible,
                "score_prediction": score_pred if series_visible else None,
                "score_hidden": score_pred is not None and not series_visible,
                "games": games_rows,
            }
        )

    return render_template(
        "player.html",
        player=player,
        is_self=is_self,
        bracket_rows=bracket_rows,
        series_rows=series_rows,
    )
