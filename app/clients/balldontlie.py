"""Minimal client for balldontlie.io's NBA API (game results). Free tier:
5 req/min, basic data - more than enough for a handful of calls per day
during the playoffs.

Docs: https://docs.balldontlie.io (Games section)
"""
import requests

BASE_URL = "https://api.balldontlie.io/v1"


def fetch_games(api_key, season, season_type="playoffs", per_page=100, session=None):
    """Fetches all games for a given season/season type (automatic
    pagination). season_type: preseason, regular, ist, playin, or playoffs.
    Returns the raw list of "game" objects as returned by the API."""
    http = session or requests
    games = []
    cursor = None
    while True:
        params = {
            "seasons[]": season,
            "season_type": season_type,
            "per_page": per_page,
        }
        if cursor is not None:
            params["cursor"] = cursor

        resp = http.get(
            f"{BASE_URL}/games",
            params=params,
            headers={"Authorization": api_key},
            timeout=20,
        )
        resp.raise_for_status()
        payload = resp.json()
        games.extend(payload["data"])

        cursor = payload.get("meta", {}).get("next_cursor")
        if not cursor:
            break

    return games
