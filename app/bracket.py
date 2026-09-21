"""Pronostics d'avant-playoffs (bracket) : champion NBA, MVP des finales,
champion de chaque conférence. Verrouillés dès qu'un match de playoffs a été
joué (voir spec - un seul pronostic par catégorie et par joueur, saisi
librement en texte faute d'une liste d'équipes/joueurs en base)."""
from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.auth import login_required
from app.extensions import db
from app.models import BracketPrediction, Game

bp = Blueprint("bracket", __name__, url_prefix="/bracket")

CATEGORIES = (
    ("nba_champion", "Champion NBA"),
    ("finals_mvp", "MVP des Finales"),
    ("east_champion", "Champion Conférence Est"),
    ("west_champion", "Champion Conférence Ouest"),
)


def _is_locked():
    return db.session.query(Game.query.filter(Game.result.isnot(None)).exists()).scalar()


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    locked = _is_locked()
    player = g.player

    if request.method == "POST":
        if locked:
            flash("Les playoffs ont commencé, le bracket est verrouillé.", "error")
            return redirect(url_for("bracket.index"))

        for key, _label in CATEGORIES:
            value = request.form.get(key, "").strip()
            if not value:
                continue
            pred = BracketPrediction.query.filter_by(player_id=player.id, category=key).first()
            if pred is None:
                pred = BracketPrediction(player_id=player.id, category=key)
                db.session.add(pred)
            pred.predicted_value = value
            pred.is_correct = None
            pred.points_earned = None
        db.session.commit()
        flash("Pronostics bracket enregistrés.", "success")
        return redirect(url_for("bracket.index"))

    existing = {
        p.category: p.predicted_value
        for p in BracketPrediction.query.filter_by(player_id=player.id).all()
    }
    return render_template("bracket.html", categories=CATEGORIES, existing=existing, locked=locked)
