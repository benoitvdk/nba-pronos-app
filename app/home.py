"""Dashboard: games and series still open for prediction for the logged-in
player, plus what they've already predicted. Once a game or series is
locked (tip-off passed / series started), every player's predictions for
that item become visible to any logged-in player - never before, so as
not to influence other players' predictions."""
from datetime import datetime, timezone

from flask import Blueprint, g, render_template

from app.auth import login_required
from app.models import Game, Player, Prediction, Series
from app.predictions import VALID_SCORES
from app.time_utils import ensure_aware_utc

bp = Blueprint("home", __name__)


def _player_prediction(player_id, prediction_type, game_id=None, series_id=None):
    return Prediction.query.filter_by(
        player_id=player_id, prediction_type=prediction_type, game_id=game_id, series_id=series_id
    ).first()


def _all_predictions(prediction_type, exclude_player_id, game_id=None, series_id=None):
    """Predictions from OTHER players (the logged-in player already sees
    their own above, no need to see themselves again in the list) for a
    game/series, sorted by name. Only call this for an item that's already
    locked (see index() below): the function itself doesn't check
    anything, it's the caller's job to guarantee nothing is revealed before
    tip-off."""
    rows = (
        Prediction.query.filter_by(
            prediction_type=prediction_type, game_id=game_id, series_id=series_id
        )
        .filter(Prediction.player_id != exclude_player_id)
        .join(Player)
        .order_by(Player.name)
        .all()
    )
    return [{"player_name": pred.player.name, "predicted_value": pred.predicted_value} for pred in rows]


@bp.route("/")
@login_required
def index():
    now = datetime.now(timezone.utc)
    player = g.player

    series_rows = []
    for series in Series.query.order_by(Series.id).all():
        started = any(gm.result is not None for gm in series.games)

        games_rows = []
        for game in series.games.order_by(Game.game_date).all():
            open_ = game.result is None and ensure_aware_utc(game.game_date) > now
            games_rows.append(
                {
                    "game": game,
                    "prediction": _player_prediction(player.id, "game_winner", game_id=game.id),
                    "open": open_,
                    "all_predictions": (
                        _all_predictions("game_winner", player.id, game_id=game.id) if not open_ else []
                    ),
                }
            )

        series_rows.append(
            {
                "series": series,
                "started": started,
                "games": games_rows,
                "winner_prediction": _player_prediction(player.id, "series_winner", series_id=series.id),
                "score_prediction": _player_prediction(player.id, "series_score", series_id=series.id),
                "all_winner_predictions": (
                    _all_predictions("series_winner", player.id, series_id=series.id) if started else []
                ),
                "all_score_predictions": (
                    _all_predictions("series_score", player.id, series_id=series.id) if started else []
                ),
            }
        )

    return render_template(
        "home.html", player=player, series_rows=series_rows, valid_scores=VALID_SCORES
    )
