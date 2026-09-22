"""Fetches game results (balldontlie) and odds (theoddsapi), and updates
the database.

Playoffs (--season-type playoffs, the default): doesn't create any Series -
they must already exist (created by hand by the admin, see README).

NBA Cup (--season-type ist): the opposite - Series are created
automatically (see app/ingestion.py.sync_cup_games_from_balldontlie),
reading the round AND group straight off balldontlie's `ist_stage` field.
Nothing else to configure - same command shape as the playoffs.

Usage:
    python -m scripts.ingest --season 2025             # test on past playoffs
    python -m scripts.ingest --season 2026              # real playoffs, once started
    python -m scripts.ingest --season 2026 --skip-odds  # without calling theoddsapi
    python -m scripts.ingest --season 2026 --season-type ist   # NBA Cup, any stage

Designed to run on a GitHub Actions cron (see .github/workflows/ingest.yml).
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
from app.ingestion import (  # noqa: E402
    sync_cup_games_from_balldontlie,
    sync_games_from_balldontlie,
    sync_odds_from_oddsapi,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--season",
        type=int,
        default=datetime.date.today().year,
        help="balldontlie season year (e.g. 2025 for the 2024-25 playoffs)",
    )
    parser.add_argument("--season-type", default="playoffs")
    parser.add_argument("--skip-odds", action="store_true", help="don't call theoddsapi.com")
    args = parser.parse_args()

    bdl_key = os.environ.get("BALLDONTLIE_API_KEY")
    if not bdl_key:
        print("BALLDONTLIE_API_KEY missing from .env", file=sys.stderr)
        sys.exit(1)

    app = create_app()
    with app.app_context():
        raw_games = fetch_games(bdl_key, season=args.season, season_type=args.season_type)
        print(f"balldontlie games fetched: {len(raw_games)}")

        if args.season_type == "ist":
            created_series, created_games, updated_games, skipped = sync_cup_games_from_balldontlie(raw_games)
            print(
                f"  series created: {created_series}, games created: {created_games}, "
                f"games updated: {updated_games}, skipped (no ist_stage): {skipped}"
            )
        else:
            created, updated, skipped = sync_games_from_balldontlie(raw_games)
            print(f"  created: {created}, updated: {updated}, skipped (no matching series): {skipped}")

        if not args.skip_odds:
            odds_key = os.environ.get("ODDS_API_KEY")
            if not odds_key:
                print("ODDS_API_KEY missing from .env, skipping odds", file=sys.stderr)
            else:
                raw_events = fetch_nba_odds(odds_key)
                odds_updated = sync_odds_from_oddsapi(raw_events)
                print(f"theoddsapi events fetched: {len(raw_events)}")
                print(f"  games updated with odds: {odds_updated}")


if __name__ == "__main__":
    main()
