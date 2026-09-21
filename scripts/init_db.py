"""Crée les tables dans la base (Neon Postgres) et initialise scoring_config
avec des valeurs de points par défaut.

Usage:
    python -m scripts.init_db

Nécessite DATABASE_URL dans l'environnement (voir .env.example). Charge
automatiquement un fichier .env s'il existe.
"""
import os
import sys

from dotenv import load_dotenv

load_dotenv()

# Permet de lancer le script depuis la racine du projet sans installer le package.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models import ScoringConfig  # noqa: E402

# Valeurs par défaut. Celles du moteur "classic" viennent de la spec ; celles du
# moteur "odds_based" sont le multiplicateur de base (1 x la cote) ; les 4 points
# de bonus "bracket" sont un point de départ à ajuster par Benoit - pas de valeur
# donnée dans la spec pour ceux-là.
DEFAULT_SCORING_CONFIG = [
    # moteur classique
    ("classic", "game_winner_points", 1),
    ("classic", "series_winner_points", 1),
    ("classic", "series_score_bonus_points", 3),
    # moteur basé sur les cotes (points = rule_value * cote du marché concerné)
    ("odds_based", "game_winner_points", 1),
    ("odds_based", "series_winner_points", 1),
    ("odds_based", "series_score_points", 1),
    # bracket pré-playoffs (à ajuster - valeurs provisoires)
    ("bracket", "nba_champion_points", 10),
    ("bracket", "finals_mvp_points", 5),
    ("bracket", "east_champion_points", 5),
    ("bracket", "west_champion_points", 5),
]


def seed_scoring_config():
    created = 0
    for engine, rule_key, rule_value in DEFAULT_SCORING_CONFIG:
        exists = ScoringConfig.query.filter_by(engine=engine, rule_key=rule_key).first()
        if exists:
            continue
        db.session.add(ScoringConfig(engine=engine, rule_key=rule_key, rule_value=rule_value))
        created += 1
    db.session.commit()
    return created


def main():
    if not os.environ.get("DATABASE_URL"):
        print(
            "DATABASE_URL manquant. Copie .env.example en .env et renseigne l'URL "
            "de connexion Neon avant de relancer ce script.",
            file=sys.stderr,
        )
        sys.exit(1)

    app = create_app()
    with app.app_context():
        db.create_all()
        print("Tables créées (ou déjà existantes).")
        created = seed_scoring_config()
        print(f"scoring_config : {created} règle(s) ajoutée(s).")


if __name__ == "__main__":
    main()
