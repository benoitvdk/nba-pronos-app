"""Turns the raw responses from the two APIs (balldontlie, theoddsapi) into
up-to-date Game rows.

For the playoffs (sync_games_from_balldontlie), this never creates a
Series: those are created by hand by the admin (see spec - the series
winner/score odds are also entered by hand). Ingestion only attaches games
to an already-existing series whose two teams match.

For the NBA Cup (sync_cup_games_from_balldontlie), it's the other way
around: since a Cup matchup is always a single game (see
app/scoring.py.is_cup_round), there's no per-series odds to enter by hand
and nothing gained by making the admin pre-create ~60 group-stage series
one by one - ingestion creates the wrapping Series itself the first time
it sees a given pairing, reading both the round AND the group straight off
balldontlie's `ist_stage` field (see _cup_round_and_group below) - no
manual input needed at all, unlike the playoffs.
"""
from datetime import datetime, timezone

from app.extensions import db
from app.models import Game, Series
from app.scoring import CUP_ROUND_PREFIX

CUP_STAGES = (
    f"{CUP_ROUND_PREFIX}group",
    f"{CUP_ROUND_PREFIX}quarterfinal",
    f"{CUP_ROUND_PREFIX}semifinal",
    f"{CUP_ROUND_PREFIX}final",
)

# balldontlie tags every NBA Cup game with an `ist_stage` field (null for
# regular season/playoff games) - confirmed against their docs (docs.
# balldontlie.io / nba.balldontlie.io), available since the 2025 season.
# It's the source of truth for both the round AND, during the group stage,
# the exact group a game belongs to (its value IS the group name) - no
# admin-maintained mapping needed, unlike what an earlier version of this
# function assumed.
_IST_STAGE_TO_ROUND = {
    "East Group A": f"{CUP_ROUND_PREFIX}group",
    "East Group B": f"{CUP_ROUND_PREFIX}group",
    "East Group C": f"{CUP_ROUND_PREFIX}group",
    "West Group A": f"{CUP_ROUND_PREFIX}group",
    "West Group B": f"{CUP_ROUND_PREFIX}group",
    "West Group C": f"{CUP_ROUND_PREFIX}group",
    "East Quarterfinal": f"{CUP_ROUND_PREFIX}quarterfinal",
    "West Quarterfinal": f"{CUP_ROUND_PREFIX}quarterfinal",
    "East Semifinal": f"{CUP_ROUND_PREFIX}semifinal",
    "West Semifinal": f"{CUP_ROUND_PREFIX}semifinal",
    "Championship": f"{CUP_ROUND_PREFIX}final",
}


def _cup_round_and_group(ist_stage):
    """Maps balldontlie's `ist_stage` value to our internal round (see
    CUP_STAGES) plus a group_name, set only for a group-stage game (its
    value is already the group's real name, e.g. "East Group A")."""
    if ist_stage not in _IST_STAGE_TO_ROUND:
        raise ValueError(f"unrecognized ist_stage: {ist_stage!r} (expected one of: {sorted(_IST_STAGE_TO_ROUND)})")
    round_ = _IST_STAGE_TO_ROUND[ist_stage]
    group_name = ist_stage if round_ == f"{CUP_ROUND_PREFIX}group" else None
    return round_, group_name


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


def _create_or_update_game(raw, series):
    """Shared by sync_games_from_balldontlie and
    sync_cup_games_from_balldontlie: creates or updates the Game row for
    `raw` under an already-resolved `series`. Returns "created" or
    "updated"."""
    home_name = raw["home_team"]["full_name"]
    away_name = raw["visitor_team"]["full_name"]

    result = None
    if raw.get("status_state") == "final":
        home_score = raw["home_team_score"]
        away_score = raw["visitor_team_score"]
        winner_name = home_name if home_score > away_score else away_name
        result = _team_side(series, winner_name)

    game_date = _parse_game_datetime(raw)
    external_id = str(raw["id"])

    game = Game.query.filter_by(external_id=external_id).first()
    status = "updated"
    if game is None:
        game = Game(
            series_id=series.id,
            team_a=series.team_a,
            team_b=series.team_b,
            game_date=game_date,
            external_id=external_id,
        )
        db.session.add(game)
        status = "created"

    game.game_date = game_date
    game.result = result
    return status


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

        if _create_or_update_game(raw, series) == "created":
            created += 1
        else:
            updated += 1

    db.session.commit()
    return created, updated, skipped


def _find_cup_series(home_name, away_name, round_, season=None):
    """Like _find_series, but only among series already tagged with this
    Cup round - keeps auto-creation from ever matching an unrelated
    playoff series between the same two teams."""
    candidates = [
        s
        for s in Series.query.filter_by(round=round_).all()
        if {s.team_a, s.team_b} == {home_name, away_name}
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


def sync_cup_games_from_balldontlie(raw_games):
    """Like sync_games_from_balldontlie, but for the NBA Cup: since a Cup
    matchup is always a single game (see app/scoring.py.is_cup_round),
    there's no reason to make the admin pre-create a Series by hand first -
    this creates the wrapping Series itself, the first time it sees a
    given pairing, tagged with the round and group balldontlie's
    `ist_stage` field reports for that game (see _cup_round_and_group) -
    unlike the playoffs, nothing here needs to be supplied by hand.

    A game with no ist_stage (shouldn't happen when fetched with
    season_type="ist", but the API's payload isn't contractually
    guaranteed) is skipped rather than failing the whole run.

    Returns (created_series, created_games, updated_games, skipped_no_stage).
    """
    created_series = created_games = updated_games = skipped = 0

    for raw in raw_games:
        ist_stage = raw.get("ist_stage")
        if not ist_stage:
            skipped += 1
            continue
        round_, group_name = _cup_round_and_group(ist_stage)

        home_name = raw["home_team"]["full_name"]
        away_name = raw["visitor_team"]["full_name"]

        series = _find_cup_series(home_name, away_name, round_, season=raw.get("season"))
        if series is None:
            series = Series(
                season=raw.get("season"),
                round=round_,
                team_a=home_name,
                team_b=away_name,
                group_name=group_name,
            )
            db.session.add(series)
            db.session.flush()  # assigns series.id, needed by _create_or_update_game
            created_series += 1

        if _create_or_update_game(raw, series) == "created":
            created_games += 1
        else:
            updated_games += 1

    db.session.commit()
    return created_series, created_games, updated_games, skipped


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
