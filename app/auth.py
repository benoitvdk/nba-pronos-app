"""Authentification simple par lien ou code d'accès, sans mot de passe
(confirmé dans la spec). Deux façons de se connecter :

- lien direct : /login/<access_code>  (celui qu'on envoie à chaque joueur)
- formulaire :  /login                (au cas où quelqu'un a juste le code)

La session est un cookie signé par SECRET_KEY (pas de table de sessions à
gérer, adapté au tier gratuit de Render).
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
    """Lien magique envoyé à chaque joueur : pas de mot de passe à saisir."""
    player = Player.query.filter_by(access_code=access_code).first()
    if player is None:
        flash("Lien invalide. Vérifie que tu as bien copié l'adresse en entier.", "error")
        return redirect(url_for("auth.login"))

    session.clear()
    session["player_id"] = player.id
    return redirect(request.args.get("next") or url_for("home.index"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Formulaire de secours si le joueur a juste son code, pas le lien complet."""
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
