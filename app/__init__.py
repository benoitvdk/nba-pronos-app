import os

from flask import Flask, send_from_directory

from app.config import Config
from app.extensions import db


def create_app(config_class=Config):
    """Flask application factory. Serves both the API and the PWA (Jinja2 +
    manifest + service worker) from a single deployment, as planned in the spec."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.models import (  # noqa: F401  (registers the models with SQLAlchemy)
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

    # Decorative team-color dot/border on prediction buttons and matchup
    # headers (see app/team_colors.py) - available as `{{ team_name | team_color }}`
    # in every template without every route having to pass it explicitly.
    from app.team_colors import team_color

    app.jinja_env.filters["team_color"] = team_color

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/sw.js")
    def service_worker():
        # Served from the root (not /static/sw.js) so the service worker can
        # control the whole app: a service worker's default scope is limited
        # to its own folder and below.
        return send_from_directory(
            os.path.join(app.static_folder), "sw.js", mimetype="application/javascript"
        )

    return app
