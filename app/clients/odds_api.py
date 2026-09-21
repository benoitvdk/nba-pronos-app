"""Minimal client for theoddsapi.com (game odds). Free tier: 500
credits/month; one daily call on this market costs about 1 credit per
region queried, well under quota (see spec).

Docs: https://the-odds-api.com/liveapi/guides/v4/
"""
import requests

BASE_URL = "https://api.the-odds-api.com/v4"
NBA_SPORT_KEY = "basketball_nba"


def fetch_nba_odds(api_key, regions="us", markets="h2h", odds_format="decimal", session=None):
    """Returns the raw list of upcoming/live NBA events with their odds
    (the API does NOT provide history on the free tier - only what's
    upcoming or live at the time of the call)."""
    http = session or requests
    resp = http.get(
        f"{BASE_URL}/sports/{NBA_SPORT_KEY}/odds",
        params={
            "apiKey": api_key,
            "regions": regions,
            "markets": markets,
            "oddsFormat": odds_format,
        },
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()
