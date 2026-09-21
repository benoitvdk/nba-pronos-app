"""Creates the tables in the database (Neon Postgres) and initializes
scoring_config with default point values.

Usage:
    python -m scripts.init_db

Requires DATABASE_URL in the environment (see .env.example).
Automatically loads a .env file if one exists.
"""
import os
import sys

from dotenv import load_dotenv

load_dotenv()

# Lets the script run from the project root without installing the package.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models import ScoringConfig  # noqa: E402

# Default values. The "classic" engine's values come from the spec; the
# "odds_based" engine's are the base multiplier (1 x the odds); the 4
# "bracket" bonus points are a starting point for Benoit to adjust - the
# spec doesn't give a value for those.
DEFAULT_SCORING_CONFIG = [
    # classic engine
    ("classic", "game_winner_points", 1),
    ("classic", "series_winner_points", 1),
    ("classic", "series_score_bonus_points", 3),
    # odds-based engine (points = rule_value * the relevant market's odds)
    ("odds_based", "game_winner_points", 1),
    ("odds_based", "series_winner_points", 1),
    ("odds_based", "series_score_points", 1),
    # pre-playoffs bracket (to adjust - provisional values)
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
            "DATABASE_URL missing. Copy .env.example to .env and fill in the "
            "Neon connection URL before running this script again.",
            file=sys.stderr,
        )
        sys.exit(1)

    app = create_app()
    with app.app_context():
        db.create_all()
        print("Tables created (or already existing).")
        created = seed_scoring_config()
        print(f"scoring_config: {created} rule(s) added.")


if __name__ == "__main__":
    main()
