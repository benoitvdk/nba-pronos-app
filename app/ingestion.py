"""Turns the raw responses from the two APIs (balldontlie, theoddsapi) into
up-to-date Game rows. Never creates a Series: those are created by hand by
the admin (see spec - the series winner/score odds are also entered by
hand). Ingestion only attaches games to an already-existing series whose
two teams match.
"""
from datetime import datetime, timezone

from app.extensions import db
from app.models import Game, Series


def _team_side(series, team_name):
    """Returns "team_a" / "team_b" depending on the match with the series,
    or None if the name doesn't match either of the series' two teams."""
    if team_name == series.team_a:
        return "team_a"
    if team_name == series.team_b:
        return "team_b"
    return None


def _find_series(home_name, away_name, season=None):
    """Looks, among the series in the database, for the one pitting these
    two teams against each other (regardless of order). If there are
    several series between the same two teams (the same two teams meeting
    again in another year), disambiguate with `season` (balldontlie season
    year); with no season given or no exact match in that case, return None
    rather than risk attaching a game to the wrong year."""
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
    # fall back to the date alone (games not yet scheduled at a precise time)
    return datetime.fromisoformat(raw_game["date"]).replace(tzinfo=timezone.utc)


def sync_games_from_balldontlie(raw_games):
    """raw_games: list of "game" objects as returned by
    app.clients.balldontlie.fetch_games. Creates or updates the
    corresponding Games. Returns (created, updated, skipped_no_series)."""
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
    """raw_events: list of events as returned by
    app.clients.odds_api.fetch_nba_odds. Only covers games not yet played
    (the API only returns upcoming/live games anyway). Takes the h2h market
    from the first available bookmaker for each event - a deliberate
    simplification (no averaging across bookmakers for now). Returns the
    number of games updated."""
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
            continue  # team names that don't match the series, skip

        # closest not-yet-played game for this series
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
