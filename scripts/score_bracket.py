"""Scores pre-tournament (bracket) predictions for a category, once the
real result is known. For the playoffs, meant to be run 4 times in total
over the course of the playoffs (as soon as a conference champion is
known, then at the end for the NBA champion and the Finals MVP); for the
NBA Cup, once per group (6) plus finalists (2) and champion (1) - see
app/bracket.py for the full list of categories per competition.

Usage:
    python -m scripts.score_bracket --category east_champion --winner "Boston Celtics"
    python -m scripts.score_bracket --category nba_champion --winner "Boston Celtics"
    python -m scripts.score_bracket --category finals_mvp --winner "Jayson Tatum"
    python -m scripts.score_bracket --category cup_east_group_a_winner --winner "Boston Celtics"
    python -m scripts.score_bracket --category cup_champion --winner "Boston Celtics"
"""
import argparse
import os
import sys

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from app.bracket import CUP_CATEGORIES, PLAYOFFS_CATEGORIES  # noqa: E402
from app.scoring_service import score_bracket_predictions  # noqa: E402

# Every category from either competition is accepted regardless of the
# server's current APP_MODE, since this is a one-off command the admin
# runs by hand once the real-world result is known.
CATEGORIES = tuple(key for key, _label in (*PLAYOFFS_CATEGORIES, *CUP_CATEGORIES))


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
