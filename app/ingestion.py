"""Transforme les réponses brutes des deux API (balldontlie, theoddsapi) en
lignes Game à jour. Ne crée jamais de Series : elles sont créées à la main
par l'admin (voir spec - les cotes vainqueur/score de série aussi sont
saisies à la main). L'ingestion ne fait que rattacher les matchs à une série
déjà existante dont les deux équipes correspondent.
"""
from datetime import datetime, timezone

from app.extensions import db
from app.models import Game, Series


def _team_side(series, team_name):
    """Renvoie "team_a" / "team_b" selon la correspondance avec la série, ou
    None si le nom ne correspond à aucune des deux équipes de la série."""
    if team_name == series.team_a:
        return "team_a"
    if team_name == series.team_b:
        return "team_b"
    return None


def _find_series(home_name, away_name, season=None):
    """Cherche, parmi les séries en base, celle qui oppose ces deux équipes
    (peu importe l'ordre). S'il y a plusieurs séries entre les deux mêmes
    équipes (les mêmes deux équipes se recroisent une autre année), on
    désambiguïse avec `season` (année de la saison balldontlie) ; sans season
    fourni ou sans correspondance exacte dans ce cas, on renvoie None plutôt
    que de risquer de rattacher un match à la mauvaise année."""
    candidates = [
        s for s in Series.query.all() if {s.team_a, s.team_b} == {home_name, away_name}
    ]
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    if season is not None:
        for s in candidates:
            if s.season == season:
                return s
    return None


def _parse_game_datetime(raw_game):
    dt = raw_game.get("datetime")
    if dt:
        return datetime.fromisoformat(dt.replace("Z", "+00:00"))
    # repli sur la date seule (matchs pas encore programmés à une heure précise)
    return datetime.fromisoformat(raw_game["date"]).replace(tzinfo=timezone.utc)


def sync_games_from_balldontlie(raw_games):
    """raw_games : liste d'objets "game" tels que renvoyés par
    app.clients.balldontlie.fetch_games. Crée ou met à jour les Game
    correspondants. Renvoie (créés, mis à jour, ignorés_pas_de_série)."""
    created = updated = skipped = 0

    for raw in raw_games:
        home_name = raw["home_team"]["full_name"]
        away_name = raw["visitor_team"]["full_name"]

        series = _find_series(home_name, away_name, season=raw.get("season"))
        if series is None:
            skipped += 1
            continue

        result = None
        if raw.get("status_state") == "final":
            home_score = raw["home_team_score"]
            away_score = raw["visitor_team_score"]
            winner_name = home_name if home_score > away_score else away_name
            result = _team_side(series, winner_name)

        game_date = _parse_game_datetime(raw)
        external_id = str(raw["id"])

        game = Game.query.filter_by(external_id=external_id).first()
        if game is None:
            game = Game(
                series_id=series.id,
                team_a=series.team_a,
                team_b=series.team_b,
                game_date=game_date,
                external_id=external_id,
            )
            db.session.add(game)
            created += 1
        else:
            updated += 1

        game.game_date = game_date
        game.result = result

    db.session.commit()
    return created, updated, skipped


def sync_odds_from_oddsapi(raw_events):
    """raw_events : liste d'events tels que renvoyés par
    app.clients.odds_api.fetch_nba_odds. Ne couvre que les matchs pas encore
    joués (l'API ne renvoie que de l'à-venir/en direct de toute façon).
    Prend le marché h2h du premier bookmaker disponible pour chaque event -
    simplification volontaire (pas de moyenne entre bookmakers pour l'instant).
    Renvoie le nombre de matchs mis à jour."""
    updated = 0

    for event in raw_events:
        home_name = event.get("home_team")
        away_name = event.get("away_team")
        if not home_name or not away_name:
            continue

        series = _find_series(home_name, away_name)
        if series is None:
            continue

        bookmakers = event.get("bookmakers") or []
        if not bookmakers:
            continue
        h2h_market = next(
            (m for m in bookmakers[0].get("markets", []) if m.get("key") == "h2h"), None
        )
        if h2h_market is None:
            continue

        prices_by_name = {o["name"]: o["price"] for o in h2h_market.get("outcomes", [])}
        odds = {}
        for team_name, price in prices_by_name.items():
            side = _team_side(series, team_name)
            if side:
                odds[side] = price
        if len(odds) != 2:
            continue  # noms d'équipe qui ne correspondent pas à la série, on ignore

        # match le pronostic pas encore joué le plus proche, pour cette série
        candidate = (
            Game.query.filter_by(series_id=series.id, result=None)
            .order_by(Game.game_date.asc())
            .first()
        )
        if candidate is None:
            continue

        candidate.game_odds = odds
        updated += 1

    db.session.commit()
    return updated
