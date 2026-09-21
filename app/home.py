"""Tableau de bord : les matchs et séries encore ouverts au pronostic pour
le joueur connecté, plus ce qu'il a déjà pronostiqué."""
from datetime import datetime, timezone

from flask import Blueprint, g, render_template

from app.auth import login_required
from app.models import Game, Prediction, Series
from app.predictions import VALID_SCORES
from app.time_utils import ensure_aware_utc

bp = Blueprint("home", __name__)


def _player_prediction(player_id, prediction_type, game_id=None, series_id=None):
    return Prediction.query.filter_by(
        player_id=player_id, prediction_type=prediction_type, game_id=game_id, series_id=series_id
    ).first()


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
            games_rows.append(
                {
                    "game": game,
                    "prediction": _player_prediction(player.id, "game_winner", game_id=game.id),
                    "open": game.result is None and ensure_aware_utc(game.game_date) > now,
                }
            )

        series_rows.append(
            {
                "series": series,
                "started": started,
                "games": games_rows,
                "winner_prediction": _player_prediction(player.id, "series_winner", series_id=series.id),
                "score_prediction": _player_prediction(player.id, "series_score", series_id=series.id),
            }
        )

    return render_template(
        "home.html", player=player, series_rows=series_rows, valid_scores=VALID_SCORES
    )
