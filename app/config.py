import os


class Config:
    """Configuration de base, lue depuis les variables d'environnement (.env en local,
    variables d'environnement Render en production)."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "")
    SQLALCHEMY_ENGINE_OPTIONS = {
        # Neon coupe les connexions inactives : on vérifie la connexion avant
        # de l'utiliser pour éviter les erreurs "server closed the connection".
        "pool_pre_ping": True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ODDS_API_KEY = os.environ.get("ODDS_API_KEY", "")
