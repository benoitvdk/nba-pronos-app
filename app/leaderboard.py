"""Leaderboard: sum of points (game/series predictions + bracket) per
player, across all engines (points are already computed with the engine
chosen at the time of scripts.run_scoring / scripts.score_bracket)."""
from collections import defaultdict
from datetime import datetime, timezone

from flask import Blueprint, g, render_template
from sqlalchemy import func

from app.auth import login_required
from app.bracket import CATEGORIES
from app.extensions import db
from app.models import BracketPrediction, Game, Player, Prediction, Series
from app.scoring import series_status
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

    # Batched instead of querying per series/game (same fix as app/home.py):
    # one query for every series' games, one for this player's predictions.
    series_list = Series.ordered_recent_first().all()
    series_ids = [series.id for series in series_list]

    games_by_series = defaultdict(list)
    for game in Game.query.filter(Game.series_id.in_(series_ids)).order_by(Game.game_date.desc()).all():
        games_by_series[game.series_id].append(game)

    preds_by_game = {}
    preds_by_series = {}
    for pred in Prediction.query.filter_by(player_id=player.id).all():
        if pred.game_id is not None:
            preds_by_game[pred.game_id] = pred
        else:
            preds_by_series[(pred.series_id, pred.prediction_type)] = pred

    series_rows = []
    for series in series_list:
        series_games = games_by_series.get(series.id, [])
        started = any(gm.result is not None for gm in series_games)
        wins_a = sum(1 for gm in series_games if gm.result == "team_a")
        wins_b = sum(1 for gm in series_games if gm.result == "team_b")
        finished = series_status(wins_a, wins_b)["finished"]
        series_visible = is_self or started

        winner_pred = preds_by_series.get((series.id, "series_winner"))
        score_pred = preds_by_series.get((series.id, "series_score"))

        # 1-indexed position of each game within the FULL series (Game 1 ..
        # Game 7), computed before games_rows below filters down to only the
        # games this player predicted - so "Game 3" still means the third
        # game of the series even if games 1 and 2 are skipped here.
        game_numbers = {
            gm.id: n for n, gm in enumerate(sorted(series_games, key=lambda gm: gm.game_date), start=1)
        }

        games_rows = []
        for game in series_games:
            game_pred = preds_by_game.get(game.id)
            if game_pred is None:
                continue
            game_open = game.result is None and ensure_aware_utc(game.game_date) > now
            game_visible = is_self or not game_open
            games_rows.append(
                {
                    "game": game,
                    "game_number": game_numbers[game.id],
                    "prediction": game_pred if game_visible else None,
                    "hidden": not game_visible,
                }
            )

        if winner_pred is None and score_pred is None and not games_rows:
            continue

        # Running point total for this series, from whatever is currently
        # visible on this profile (own profile: everything; someone else's:
        # only what's already unlocked) - matches what's actually displayed
        # below, so it can't leak a not-yet-revealed result.
        total_points = sum(
            float(gr["prediction"].points_earned or 0) for gr in games_rows if gr["prediction"]
        )
        if series_visible:
            if winner_pred:
                total_points += float(winner_pred.points_earned or 0)
            if score_pred:
                total_points += float(score_pred.points_earned or 0)

        series_rows.append(
            {
                "series": series,
                "started": started,
                "finished": finished,
                "winner_prediction": winner_pred if series_visible else None,
                "winner_hidden": winner_pred is not None and not series_visible,
                "score_prediction": score_pred if series_visible else None,
                "score_hidden": score_pred is not None and not series_visible,
                "games": games_rows,
                "total_points": total_points,
            }
        )

    return render_template(
        "player.html",
        player=player,
        is_self=is_self,
        bracket_rows=bracket_rows,
        series_rows=series_rows,
    )
