"""Scores pre-playoffs (bracket) predictions for a category, once the real
result is known. Meant to be run 4 times in total over the course of the
playoffs (as soon as a conference champion is known, then at the end for
the NBA champion and the Finals MVP).

Usage:
    python -m scripts.score_bracket --category east_champion --winner "Boston Celtics"
    python -m scripts.score_bracket --category nba_champion --winner "Boston Celtics"
    python -m scripts.score_bracket --category finals_mvp --winner "Jayson Tatum"
"""
import argparse
import os
import sys

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from app.scoring_service import score_bracket_predictions  # noqa: E402

CATEGORIES = ("nba_champion", "finals_mvp", "east_champion", "west_champion")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", choices=CATEGORIES, required=True)
    parser.add_argument("--winner", required=True, help="Actual value (must exactly match the submitted predictions)")
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        updated = score_bracket_predictions(args.category, args.winner)

    print(f"Category: {args.category}")
    print(f"Result recorded: {args.winner}")
    print(f"Predictions scored: {updated}")


if __name__ == "__main__":
    main()
