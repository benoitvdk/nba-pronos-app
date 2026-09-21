from flask_sqlalchemy import SQLAlchemy

# Instance partagée, initialisée par l'application factory (app/__init__.py)
# et importée par les modèles (app/models.py) et les scripts (scripts/init_db.py).
db = SQLAlchemy()
