"""Pre-tournament (bracket) predictions, locked as soon as the first game
of the current competition has been played (see spec - one prediction per
category and per player, entered as free text since there's no list of
teams/players in the database).

Which categories are on offer depends on APP_MODE (see app/config.py):
NBA champion / Finals MVP / conference champions for the playoffs, or NBA
Cup champion / finalists / group winners for the Cup - the two never show
at once, and `is_locked()` only looks at games from the current
competition's rounds, so switching modes on the same database never
locks/unlocks the wrong set (see app/scoring.py.is_cup_round)."""
from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for

from app.auth import login_required
from app.extensions import db
from app.models import BracketPrediction, Game, Series
from app.scoring import CUP_ROUND_PREFIX

bp = Blueprint("bracket", __name__, url_prefix="/bracket")

PLAYOFFS_CATEGORIES = (
    ("nba_champion", "Champion NBA"),
    ("finals_mvp", "MVP des Finales"),
    ("east_champion", "Champion Conférence Est"),
    ("west_champion", "Champion Conférence Ouest"),
)

# The real 2026-27 groups (3 per conference, A/B/C - see NBA.com's
# official announcement) match this A/B/C-per-conference shape, so these
# category keys don't need touching season to season; only the point
# values below are provisional.
CUP_CATEGORIES = (
    ("cup_champion", "Vainqueur de la NBA Cup"),
    ("cup_finalist_east", "Finaliste Conférence Est"),
    ("cup_finalist_west", "Finaliste Conférence Ouest"),
    ("cup_east_group_a_winner", "Vainqueur Groupe A (Est)"),
    ("cup_east_group_b_winner", "Vainqueur Groupe B (Est)"),
    ("cup_east_group_c_winner", "Vainqueur Groupe C (Est)"),
    ("cup_west_group_a_winner", "Vainqueur Groupe A (Ouest)"),
    ("cup_west_group_b_winner", "Vainqueur Groupe B (Ouest)"),
    ("cup_west_group_c_winner", "Vainqueur Groupe C (Ouest)"),
)


def _cup_mode():
    return current_app.config.get("APP_MODE") == "nba_cup"


def get_categories():
    return CUP_CATEGORIES if _cup_mode() else PLAYOFFS_CATEGORIES


def is_locked():
    """True once a game from the CURRENT competition (playoffs or Cup,
    whichever APP_MODE selects) has been played - a Cup game played in a
    prior season, sitting in the same database, must never lock the
    playoffs bracket, and vice versa."""
    round_filter = Series.round.like(f"{CUP_ROUND_PREFIX}%") if _cup_mode() else ~Series.round.like(f"{CUP_ROUND_PREFIX}%")
    return db.session.query(
        Game.query.join(Series).filter(Game.result.isnot(None), round_filter).exists()
    ).scalar()


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    locked = is_locked()
    categories = get_categories()
    player = g.player

    if request.method == "POST":
        if locked:
            flash("La compétition a commencé, le bracket est verrouillé.", "error")
            return redirect(url_for("bracket.index"))

        for key, _label in categories:
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
    return render_template("bracket.html", categories=categories, existing=existing, locked=locked)
