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
