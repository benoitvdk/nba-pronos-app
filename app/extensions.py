from flask_sqlalchemy import SQLAlchemy

# Shared instance, initialized by the application factory (app/__init__.py)
# and imported by the models (app/models.py) and the scripts (scripts/init_db.py).
db = SQLAlchemy()
