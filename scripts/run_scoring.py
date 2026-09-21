"""Recomputes points for all already-determinable game and series
predictions, with the chosen engine.

Usage:
    python -m scripts.run_scoring --engine classic
    python -m scripts.run_scoring --engine odds_based
"""
import argparse
import os
import sys

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from app.scoring import ENGINES  # noqa: E402
from app.scoring_service import score_game_predictions, score_series_predictions  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", choices=ENGINES, default="classic")
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        games_updated = score_game_predictions(engine=args.engine)
        series_updated = score_series_predictions(engine=args.engine)

    print(f"Engine: {args.engine}")
    print(f"Game predictions scored:   {games_updated}")
    print(f"Series predictions scored: {series_updated}")


if __name__ == "__main__":
    main()
