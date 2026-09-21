"""Client minimal pour theoddsapi.com (cotes des matchs). Palier gratuit :
500 crédits/mois ; un appel quotidien sur ce marché coûte environ 1 crédit
par région interrogée, largement sous le quota (voir spec).

Doc : https://the-odds-api.com/liveapi/guides/v4/
"""
import requests

BASE_URL = "https://api.the-odds-api.com/v4"
NBA_SPORT_KEY = "basketball_nba"


def fetch_nba_odds(api_key, regions="us", markets="h2h", odds_format="decimal", session=None):
    """Renvoie la liste brute des events NBA à venir/en cours avec leurs
    cotes (l'API ne donne PAS d'historique sur le palier gratuit - seulement
    ce qui est à venir ou en direct au moment de l'appel)."""
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
