import os


def _normalize_db_url(url):
    """Forces the psycopg2 driver (the one in requirements.txt), whatever
    was pasted in DATABASE_URL: Neon's SQLAlchemy snippet gives
    "postgresql+psycopg://" (psycopg 3, not installed), some hosts give
    "postgres://", and secrets sometimes carry stray spaces or quotes."""
    url = url.strip().strip("'\"").strip()
    if not url:
        return url
    scheme, sep, rest = url.partition("://")
    if sep and scheme.lower().split("+")[0] in ("postgres", "postgresql"):
        return "postgresql+psycopg2://" + rest
    return url


class Config:
    """Base configuration, read from environment variables (.env locally,
    Render environment variables in production)."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")

    SQLALCHEMY_DATABASE_URI = _normalize_db_url(os.environ.get("DATABASE_URL", ""))
    SQLALCHEMY_ENGINE_OPTIONS = {
        # Neon drops idle connections: check the connection before using it
        # to avoid "server closed the connection" errors.
        "pool_pre_ping": True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ODDS_API_KEY = os.environ.get("ODDS_API_KEY", "")
