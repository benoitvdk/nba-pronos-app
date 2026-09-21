"""Soumission des pronostics par les joueurs : match par match, vainqueur de
série, et score exact de série (équipe + score combinés - voir
app/scoring.py `series_score_key`). Un pronostic peut être modifié tant que
le match/la série n'a pas commencé."""
from datetime import datetime, timezone

from flask import Blueprint, abort, flash, g, redirect, request, url_for

from app.auth import login_required
from app.extensions import db
from app.models import Game, Prediction, Series
from app.scoring import series_score_key
from app.time_utils import ensure_aware_utc

bp = Blueprint("predictions", __name__, url_prefix="/predict")

VALID_SCORES = ("4-0", "4-1", "4-2", "4-3")


def _upsert_prediction(player_id, prediction_type, predicted_value, game_id=None, series_id=None):
    query = Prediction.query.filter_by(
        player_id=player_id, prediction_type=prediction_type, game_id=game_id, series_id=series_id
    )
    pred = query.first()
    if pred is None:
        pred = Prediction(
            player_id=player_id,
            prediction_type=prediction_type,
            game_id=game_id,
            series_id=series_id,
        )
        db.session.add(pred)
    pred.predicted_value = predicted_value
    # un nouveau pronostic (ou une modification) n'est pas encore noté
    pred.is_correct = None
    pred.points_earned = None
    db.session.commit()


@bp.post("/game/<int:game_id>")
@login_required
def predict_game(game_id):
    game = db.get_or_404(Game, game_id)
    side = request.form.get("side")
    if side not in ("team_a", "team_b"):
        flash("Choix invalide.", "error")
        return redirect(url_for("home.index"))

    if game.result is not None:
        flash("Ce match est déjà terminé, pronostic fermé.", "error")
        return redirect(url_for("home.index"))
    if ensure_aware_utc(game.game_date) <= datetime.now(timezone.utc):
        flash("Ce match a déjà commencé, pronostic fermé.", "error")
        return redirect(url_for("home.index"))

    _upsert_prediction(g.player.id, "game_winner", side, game_id=game.id)
    team_name = game.team_a if side == "team_a" else game.team_b
    flash(f"Pronostic enregistré : {team_name} gagne.", "success")
    return redirect(url_for("home.index"))


@bp.post("/series/<int:series_id>/winner")
@login_required
def predict_series_winner(series_id):
    series = db.get_or_404(Series, series_id)
    side = request.form.get("side")
    if side not in ("team_a", "team_b"):
        flash("Choix invalide.", "error")
        return redirect(url_for("home.index"))

    if any(gm.result is not None for gm in series.games):
        flash("Cette série a déjà commencé, pronostic vainqueur fermé.", "error")
        return redirect(url_for("home.index"))

    _upsert_prediction(g.player.id, "series_winner", side, series_id=series.id)
    team_name = series.team_a if side == "team_a" else series.team_b
    flash(f"Pronostic enregistré : {team_name} remporte la série.", "success")
    return redirect(url_for("home.index"))


@bp.post("/series/<int:series_id>/score")
@login_required
def predict_series_score(series_id):
    series = db.get_or_404(Series, series_id)
    side = request.form.get("side")
    score = request.form.get("score")
    if side not in ("team_a", "team_b") or score not in VALID_SCORES:
        flash("Choix invalide.", "error")
        return redirect(url_for("home.index"))

    if any(gm.result is not None for gm in series.games):
        flash("Cette série a déjà commencé, pronostic score fermé.", "error")
        return redirect(url_for("home.index"))

    predicted_value = series_score_key(side, score)
    _upsert_prediction(g.player.id, "series_score", predicted_value, series_id=series.id)
    team_name = series.team_a if side == "team_a" else series.team_b
    flash(f"Pronostic enregistré : {team_name} gagne {score}.", "success")
    return redirect(url_for("home.index"))
