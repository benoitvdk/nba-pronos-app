"""Tableau de bord : les matchs et séries encore ouverts au pronostic pour
le joueur connecté, plus ce qu'il a déjà pronostiqué. Une fois un match ou
une série verrouillé(e) (coup d'envoi passé / série commencée), les
pronostics de tous les joueurs pour cet élément deviennent visibles par
n'importe quel joueur connecté - jamais avant, pour ne pas influencer les
pronostics des autres."""
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


def _all_predictions(prediction_type, game_id=None, series_id=None):
    """Pronostics de tous les joueurs pour un match/une série, triés par nom.
    À n'appeler que pour un élément déjà verrouillé (voir index() ci-dessous) :
    la fonction elle-même ne vérifie rien, c'est l'appelant qui garantit que
    rien n'est révélé avant le coup d'envoi."""
    rows = (
        Prediction.query.filter_by(
            prediction_type=prediction_type, game_id=game_id, series_id=series_id
        )
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
                        _all_predictions("game_winner", game_id=game.id) if not open_ else []
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
                    _all_predictions("series_winner", series_id=series.id) if started else []
                ),
                "all_score_predictions": (
                    _all_predictions("series_score", series_id=series.id) if started else []
                ),
            }
        )

    return render_template(
        "home.html", player=player, series_rows=series_rows, valid_scores=VALID_SCORES
    )
