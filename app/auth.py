"""Simple authentication via link or access code, no password (confirmed
in the spec). Two ways to log in:

- direct link: /login/<access_code>  (the one sent to each player)
- form:        /login                (in case someone only has the code)

The session is a cookie signed with SECRET_KEY (no session table to
manage, well suited to Render's free tier).
"""
from functools import wraps

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.extensions import db
from app.models import Player

bp = Blueprint("auth", __name__)


@bp.before_app_request
def load_logged_in_player():
    player_id = session.get("player_id")
    g.player = db.session.get(Player, player_id) if player_id else None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.player is None:
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


@bp.route("/login/<access_code>")
def login_via_link(access_code):
    """Magic link sent to each player: no password to enter."""
    player = Player.query.filter_by(access_code=access_code).first()
    if player is None:
        flash("Lien invalide. Vérifie que tu as bien copié l'adresse en entier.", "error")
        return redirect(url_for("auth.login"))

    session.clear()
    session["player_id"] = player.id
    return redirect(request.args.get("next") or url_for("home.index"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Fallback form for a player who only has their code, not the full link."""
    if request.method == "POST":
        code = request.form.get("access_code", "").strip()
        player = Player.query.filter_by(access_code=code).first() if code else None
        if player is None:
            flash("Code invalide.", "error")
        else:
            session.clear()
            session["player_id"] = player.id
            return redirect(request.args.get("next") or url_for("home.index"))
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
