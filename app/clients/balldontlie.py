"""Client minimal pour l'API NBA de balldontlie.io (résultats de matchs).
Palier gratuit : 5 req/min, données de base - largement suffisant pour un
usage à raison de quelques appels par jour pendant les playoffs.

Doc : https://docs.balldontlie.io (section Games)
"""
import requests

BASE_URL = "https://api.balldontlie.io/v1"


def fetch_games(api_key, season, season_type="playoffs", per_page=100, session=None):
    """Récupère tous les matchs d'une saison/type de saison donnés (pagination
    automatique). season_type: preseason, regular, ist, playin, ou playoffs.
    Renvoie la liste brute des objets "game" tels que renvoyés par l'API."""
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
