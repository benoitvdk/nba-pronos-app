"""Note les pronostics d'avant-playoffs (bracket) d'une catégorie, une fois
le résultat réel connu. À lancer 4 fois en tout au fil des playoffs (dès
qu'un champion de conférence est connu, puis à la fin pour le champion NBA
et le MVP des finales).

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
    parser.add_argument("--winner", required=True, help="Valeur réelle (doit correspondre exactement aux pronostics saisis)")
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        updated = score_bracket_predictions(args.category, args.winner)

    print(f"Catégorie : {args.category}")
    print(f"Résultat retenu : {args.winner}")
    print(f"Pronostics notés : {updated}")


if __name__ == "__main__":
    main()
