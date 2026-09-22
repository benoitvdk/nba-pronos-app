import os


class Config:
    """Base configuration, read from environment variables (.env locally,
    Render environment variables in production)."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "")
    SQLALCHEMY_ENGINE_OPTIONS = {
        # Neon drops idle connections: check the connection before using it
        # to avoid "server closed the connection" errors.
        "pool_pre_ping": True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ODDS_API_KEY = os.environ.get("ODDS_API_KEY", "")

    # "playoffs" or "nba_cup" - the app only ever runs one competition at a
    # time (see README), this picks which one: labels, bracket categories
    # (app/bracket.py) and which Series/Game rows show up anywhere in the
    # app (app/home.py, app/leaderboard.py - see app/scoring.py.is_cup_round).
    APP_MODE = os.environ.get("APP_MODE", "playoffs")
