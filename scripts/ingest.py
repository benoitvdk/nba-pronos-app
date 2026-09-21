"""Récupère les résultats de matchs (balldontlie) et les cotes (theoddsapi),
et met à jour la base. Ne crée aucune Series - elles doivent déjà exister
(créées à la main par l'admin, voir README).

Usage:
    python -m scripts.ingest --season 2025             # test sur les playoffs passés
    python -m scripts.ingest --season 2026              # vrais playoffs, une fois commencés
    python -m scripts.ingest --season 2026 --skip-odds  # sans appeler theoddsapi

Pensé pour tourner sur un cron GitHub Actions (voir .github/workflows/ingest.yml).
"""
import argparse
import datetime
import os
import sys

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from app.clients.balldontlie import fetch_games  # noqa: E402
from app.clients.odds_api import fetch_nba_odds  # noqa: E402
from app.ingestion import sync_games_from_balldontlie, sync_odds_from_oddsapi  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--season",
        type=int,
        default=datetime.date.today().year,
        help="année de saison balldontlie (ex: 2025 pour les playoffs 2024-25)",
    )
    parser.add_argument("--season-type", default="playoffs")
    parser.add_argument("--skip-odds", action="store_true", help="ne pas appeler theoddsapi.com")
    args = parser.parse_args()

    bdl_key = os.environ.get("BALLDONTLIE_API_KEY")
    if not bdl_key:
        print("BALLDONTLIE_API_KEY manquant dans .env", file=sys.stderr)
        sys.exit(1)

    app = create_app()
    with app.app_context():
        raw_games = fetch_games(bdl_key, season=args.season, season_type=args.season_type)
        created, updated, skipped = sync_games_from_balldontlie(raw_games)
        print(f"Matchs balldontlie récupérés : {len(raw_games)}")
        print(f"  créés : {created}, mis à jour : {updated}, ignorés (pas de série correspondante) : {skipped}")

        if not args.skip_odds:
            odds_key = os.environ.get("ODDS_API_KEY")
            if not odds_key:
                print("ODDS_API_KEY manquant dans .env, cotes ignorées", file=sys.stderr)
            else:
                raw_events = fetch_nba_odds(odds_key)
                odds_updated = sync_odds_from_oddsapi(raw_events)
                print(f"Events theoddsapi récupérés : {len(raw_events)}")
                print(f"  matchs mis à jour avec des cotes : {odds_updated}")


if __name__ == "__main__":
    main()
