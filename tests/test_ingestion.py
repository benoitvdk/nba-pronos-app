"""Tests for ingestion (app/ingestion.py) with fake data that matches the
exact shape of balldontlie.io / theoddsapi.com responses (see their
official docs), and for the HTTP clients (app/clients/*) with requests
mocked - no real network call here."""
import os
from unittest.mock import MagicMock

import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret")

from app import create_app  # noqa: E402
from app.clients.balldontlie import fetch_games  # noqa: E402
from app.clients.odds_api import fetch_nba_odds  # noqa: E402
from app.extensions import db  # noqa: E402
from app.ingestion import (  # noqa: E402
    sync_cup_games_from_balldontlie,
    sync_games_from_balldontlie,
    sync_odds_from_oddsapi,
)
from app.models import Game, Series  # noqa: E402


@pytest.fixture
def app():
    flask_app = create_app()
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


def _raw_game(game_id, home, away, status_state="scheduled", home_score=0, away_score=0, date="2025-05-20"):
    return {
        "id": game_id,
        "date": date,
        "season": 2024,
        "status": "Final" if status_state == "final" else "Scheduled",
        "status_state": status_state,
        "postseason": True,
        "postponed": False,
        "home_team_score": home_score,
        "visitor_team_score": away_score,
        "datetime": f"{date}T23:00:00.000Z",
        "home_team": {"id": 2, "full_name": home, "abbreviation": home[:3].upper()},
        "visitor_team": {"id": 7, "full_name": away, "abbreviation": away[:3].upper()},
    }


def _raw_odds_event(home, away, home_price, away_price):
    return {
        "id": "evt1",
        "sport_key": "basketball_nba",
        "commence_time": "2025-05-21T23:00:00Z",
        "home_team": home,
        "away_team": away,
        "bookmakers": [
            {
                "key": "fanduel",
                "title": "FanDuel",
                "last_update": "2025-05-20T10:00:00Z",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": home, "price": home_price},
                            {"name": away, "price": away_price},
                        ],
                    }
                ],
            }
        ],
    }


# --- sync_games_from_balldontlie -----------------------------------------

def test_sync_creates_game_for_matching_series(app):
    series = Series(round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()

    raw = [_raw_game(101, "Boston Celtics", "Denver Nuggets", status_state="scheduled")]
    created, updated, skipped = sync_games_from_balldontlie(raw)

    assert (created, updated, skipped) == (1, 0, 0)
    game = Game.query.filter_by(external_id="101").first()
    assert game is not None
    assert game.series_id == series.id
    assert game.result is None


def test_sync_sets_result_using_series_team_order(app):
    # the series has team_a = Nuggets while balldontlie gives Nuggets as "visitor"
    series = Series(round="finals", team_a="Denver Nuggets", team_b="Boston Celtics")
    db.session.add(series)
    db.session.commit()

    raw = [
        _raw_game(
            102, home="Boston Celtics", away="Denver Nuggets",
            status_state="final", home_score=110, away_score=101,
        )
    ]
    sync_games_from_balldontlie(raw)

    game = Game.query.filter_by(external_id="102").first()
    assert game.result == "team_b"  # Boston (winner) == series.team_b


def test_sync_is_idempotent_no_duplicate_on_rerun(app):
    series = Series(round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()

    raw = [_raw_game(103, "Boston Celtics", "Denver Nuggets", status_state="scheduled")]
    sync_games_from_balldontlie(raw)
    # the game finishes, re-run with the same list (unchanged id)
    raw[0].update(status_state="final", home_team_score=100, visitor_team_score=90)
    created, updated, skipped = sync_games_from_balldontlie(raw)

    assert (created, updated, skipped) == (0, 1, 0)
    assert Game.query.filter_by(external_id="103").count() == 1
    assert Game.query.filter_by(external_id="103").first().result == "team_a"


def test_sync_skips_games_without_matching_series(app):
    # no series at all in the database
    raw = [_raw_game(104, "Boston Celtics", "Denver Nuggets")]
    created, updated, skipped = sync_games_from_balldontlie(raw)
    assert (created, updated, skipped) == (0, 0, 1)


def test_sync_disambiguates_same_matchup_across_seasons(app):
    # the same two teams met again in two different years
    old_series = Series(season=2023, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    new_series = Series(season=2024, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add_all([old_series, new_series])
    db.session.commit()

    raw = [_raw_game(105, "Boston Celtics", "Denver Nuggets", status_state="scheduled")]
    # _raw_game defaults to season=2024
    created, updated, skipped = sync_games_from_balldontlie(raw)

    assert (created, updated, skipped) == (1, 0, 0)
    game = Game.query.filter_by(external_id="105").first()
    assert game.series_id == new_series.id


def test_sync_skips_ambiguous_matchup_without_season_match(app):
    db.session.add_all(
        [
            Series(season=2022, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets"),
            Series(season=2023, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets"),
        ]
    )
    db.session.commit()

    raw = [_raw_game(106, "Boston Celtics", "Denver Nuggets")]  # season=2024, matches neither
    created, updated, skipped = sync_games_from_balldontlie(raw)
    assert (created, updated, skipped) == (0, 0, 1)


# --- sync_cup_games_from_balldontlie ---------------------------------------

def test_sync_cup_creates_series_and_group_name_on_first_sight(app):
    raw = [_raw_game(301, "Boston Celtics", "Miami Heat", status_state="scheduled")]
    groups = {"Boston Celtics": "Groupe A (Est)", "Miami Heat": "Groupe A (Est)"}

    created_series, created_games, updated_games = sync_cup_games_from_balldontlie(
        raw, stage="cup_group", groups=groups
    )

    assert (created_series, created_games, updated_games) == (1, 1, 0)
    series = Series.query.filter_by(round="cup_group").one()
    assert {series.team_a, series.team_b} == {"Boston Celtics", "Miami Heat"}
    assert series.group_name == "Groupe A (Est)"
    game = Game.query.filter_by(external_id="301").first()
    assert game.series_id == series.id


def test_sync_cup_is_idempotent_no_duplicate_series_or_game(app):
    raw = [_raw_game(302, "Boston Celtics", "Miami Heat", status_state="scheduled")]
    sync_cup_games_from_balldontlie(raw, stage="cup_group")
    raw[0].update(status_state="final", home_team_score=100, visitor_team_score=90)

    created_series, created_games, updated_games = sync_cup_games_from_balldontlie(raw, stage="cup_group")

    assert (created_series, created_games, updated_games) == (0, 0, 1)
    assert Series.query.filter_by(round="cup_group").count() == 1
    assert Game.query.filter_by(external_id="302").first().result == "team_a"


def test_sync_cup_does_not_reuse_a_playoff_series_between_the_same_teams(app):
    # Same two teams, but this is a playoff series - the Cup ingestion must
    # never attach a group-stage game to it.
    db.session.add(Series(round="finals", team_a="Boston Celtics", team_b="Miami Heat"))
    db.session.commit()

    raw = [_raw_game(303, "Boston Celtics", "Miami Heat", status_state="scheduled")]
    created_series, created_games, updated_games = sync_cup_games_from_balldontlie(raw, stage="cup_group")

    assert created_series == 1
    assert Series.query.filter_by(round="cup_group").count() == 1
    assert Series.query.filter_by(round="finals").count() == 1


def test_sync_cup_group_name_only_set_for_group_stage(app):
    raw = [_raw_game(304, "Boston Celtics", "Miami Heat", status_state="scheduled")]
    groups = {"Boston Celtics": "Groupe A (Est)"}

    sync_cup_games_from_balldontlie(raw, stage="cup_quarterfinal", groups=groups)

    series = Series.query.filter_by(round="cup_quarterfinal").one()
    assert series.group_name is None


def test_sync_cup_team_missing_from_groups_map_leaves_group_name_none(app):
    raw = [_raw_game(305, "Boston Celtics", "Miami Heat", status_state="scheduled")]
    created_series, _, _ = sync_cup_games_from_balldontlie(raw, stage="cup_group", groups={})
    assert created_series == 1
    assert Series.query.filter_by(round="cup_group").one().group_name is None


def test_sync_cup_rejects_unknown_stage(app):
    with pytest.raises(ValueError):
        sync_cup_games_from_balldontlie([], stage="cup_wildcard")


# --- sync_odds_from_oddsapi ------------------------------------------------

def test_sync_odds_updates_next_unplayed_game(app):
    series = Series(round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()
    sync_games_from_balldontlie(
        [_raw_game(201, "Boston Celtics", "Denver Nuggets", status_state="scheduled", date="2025-05-22")]
    )

    events = [_raw_odds_event("Boston Celtics", "Denver Nuggets", home_price=1.65, away_price=2.3)]
    updated = sync_odds_from_oddsapi(events)

    assert updated == 1
    game = Game.query.filter_by(external_id="201").first()
    assert game.game_odds == {"team_a": 1.65, "team_b": 2.3}


def test_sync_odds_ignores_event_with_no_matching_series(app):
    events = [_raw_odds_event("Miami Heat", "New York Knicks", home_price=1.5, away_price=2.5)]
    updated = sync_odds_from_oddsapi(events)
    assert updated == 0


# --- clients (requests mocked, no network call) ----------------------------

def test_fetch_games_paginates_and_sends_auth_header():
    page1 = MagicMock()
    page1.json.return_value = {"data": [{"id": 1}], "meta": {"next_cursor": 50}}
    page1.raise_for_status.return_value = None
    page2 = MagicMock()
    page2.json.return_value = {"data": [{"id": 2}], "meta": {"next_cursor": None}}
    page2.raise_for_status.return_value = None

    session = MagicMock()
    session.get.side_effect = [page1, page2]

    games = fetch_games("test-key", season=2025, session=session)

    assert [g["id"] for g in games] == [1, 2]
    first_call_kwargs = session.get.call_args_list[0].kwargs
    assert first_call_kwargs["headers"] == {"Authorization": "test-key"}
    assert first_call_kwargs["params"]["seasons[]"] == 2025


def test_fetch_nba_odds_sends_api_key_and_returns_json():
    resp = MagicMock()
    resp.json.return_value = [{"id": "evt1"}]
    resp.raise_for_status.return_value = None
    session = MagicMock()
    session.get.return_value = resp

    events = fetch_nba_odds("odds-key", session=session)

    assert events == [{"id": "evt1"}]
    call_kwargs = session.get.call_args.kwargs
    assert call_kwargs["params"]["apiKey"] == "odds-key"
