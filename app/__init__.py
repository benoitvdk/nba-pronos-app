import os

from flask import Flask, send_from_directory

from app.config import Config
from app.extensions import db


def create_app(config_class=Config):
    """Application factory Flask. Sert à la fois l'API et la PWA (Jinja2 + manifest
    + service worker) depuis un seul déploiement, comme prévu dans la spec."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.models import (  # noqa: F401  (enregistre les modèles auprès de SQLAlchemy)
        Player,
        Series,
        Game,
        Prediction,
        ScoringConfig,
        BracketPrediction,
    )

    from app.auth import bp as auth_bp
    from app.home import bp as home_bp
    from app.predictions import bp as predictions_bp
    from app.leaderboard import bp as leaderboard_bp
    from app.bracket import bp as bracket_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(predictions_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(bracket_bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/sw.js")
    def service_worker():
        # Servi depuis la racine (pas /static/sw.js) pour que le service worker
        # puisse contrôler toute l'app : la portée par défaut d'un service
        # worker se limite à son propre dossier et en dessous.
        return send_from_directory(
            os.path.join(app.static_folder), "sw.js", mimetype="application/javascript"
        )

    return app
