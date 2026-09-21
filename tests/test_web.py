"""Tests for the web routes: predictions (game/series), leaderboard,
bracket. Uses the Flask test client, in-memory SQLite database - no real
server."""
import os
from datetime import datetime, timedelta, timezone

import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret")

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models import BracketPrediction, Game, Player, Prediction, Series  # noqa: E402

FUTURE = datetime.now(timezone.utc) + timedelta(days=1)
PAST = datetime.now(timezone.utc) - timedelta(days=1)


@pytest.fixture
def app():
    flask_app = create_app()
    flask_app.config.update(TESTING=True)
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def player(app):
    p = Player(name="Alice", access_code="alice-code")
    db.session.add(p)
    db.session.commit()
    return p


def _login(client, player):
    client.get(f"/login/{player.access_code}")


# --- game prediction ----------------------------------------------------

def test_predict_game_creates_prediction(app, client, player):
    series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()
    game = Game(series_id=series.id, team_a="Boston Celtics", team_b="Denver Nuggets", game_date=FUTURE)
    db.session.add(game)
    db.session.commit()

    _login(client, player)
    resp = client.post(f"/predict/game/{game.id}", data={"side": "team_a"}, follow_redirects=True)

    assert resp.status_code == 200
    pred = Prediction.query.filter_by(player_id=player.id, game_id=game.id).first()
    assert pred is not None
    assert pred.predicted_value == "team_a"
    assert pred.is_correct is None  # not scored yet


def test_predict_game_rejected_once_played(app, client, player):
    series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()
    game = Game(
        series_id=series.id, team_a="Boston Celtics", team_b="Denver Nuggets",
        game_date=PAST, result="team_a",
    )
    db.session.add(game)
    db.session.commit()

    _login(client, player)
    client.post(f"/predict/game/{game.id}", data={"side": "team_b"}, follow_redirects=True)

    assert Prediction.query.filter_by(player_id=player.id, game_id=game.id).first() is None


def test_predict_game_rejected_once_started(app, client, player):
    series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()
    game = Game(series_id=series.id, team_a="Boston Celtics", team_b="Denver Nuggets", game_date=PAST)
    db.session.add(game)
    db.session.commit()

    _login(client, player)
    client.post(f"/predict/game/{game.id}", data={"side": "team_a"}, follow_redirects=True)

    assert Prediction.query.filter_by(player_id=player.id, game_id=game.id).first() is None


def test_predict_game_requires_login(app, client):
    series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()
    game = Game(series_id=series.id, team_a="Boston Celtics", team_b="Denver Nuggets", game_date=FUTURE)
    db.session.add(game)
    db.session.commit()

    resp = client.post(f"/predict/game/{game.id}", data={"side": "team_a"}, follow_redirects=False)
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


# --- series prediction (winner + score combined) ------------------------

def test_predict_series_winner_and_score(app, client, player):
    series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()

    _login(client, player)
    client.post(f"/predict/series/{series.id}/winner", data={"side": "team_b"}, follow_redirects=True)
    client.post(
        f"/predict/series/{series.id}/score", data={"side": "team_b", "score": "4-2"}, follow_redirects=True
    )

    winner_pred = Prediction.query.filter_by(
        player_id=player.id, series_id=series.id, prediction_type="series_winner"
    ).first()
    score_pred = Prediction.query.filter_by(
        player_id=player.id, series_id=series.id, prediction_type="series_score"
    ).first()
    assert winner_pred.predicted_value == "team_b"
    assert score_pred.predicted_value == "team_b:4-2"


def test_predict_series_rejected_once_started(app, client, player):
    series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()
    db.session.add(
        Game(series_id=series.id, team_a="Boston Celtics", team_b="Denver Nuggets", game_date=PAST, result="team_a")
    )
    db.session.commit()

    _login(client, player)
    client.post(f"/predict/series/{series.id}/winner", data={"side": "team_a"}, follow_redirects=True)

    assert (
        Prediction.query.filter_by(
            player_id=player.id, series_id=series.id, prediction_type="series_winner"
        ).first()
        is None
    )


def test_predict_updates_existing_prediction_instead_of_duplicating(app, client, player):
    series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()

    _login(client, player)
    client.post(f"/predict/series/{series.id}/winner", data={"side": "team_a"}, follow_redirects=True)
    client.post(f"/predict/series/{series.id}/winner", data={"side": "team_b"}, follow_redirects=True)

    preds = Prediction.query.filter_by(
        player_id=player.id, series_id=series.id, prediction_type="series_winner"
    ).all()
    assert len(preds) == 1
    assert preds[0].predicted_value == "team_b"


# --- leaderboard -----------------------------------------------------------

def test_leaderboard_sums_prediction_and_bracket_points(app, client, player):
    other = Player(name="Bob", access_code="bob-code")
    db.session.add(other)
    db.session.commit()

    series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()
    game = Game(series_id=series.id, team_a="Boston Celtics", team_b="Denver Nuggets", game_date=PAST, result="team_a")
    db.session.add(game)
    db.session.commit()

    db.session.add(
        Prediction(
            player_id=player.id, game_id=game.id, prediction_type="game_winner",
            predicted_value="team_a", is_correct=True, points_earned=1,
        )
    )
    db.session.add(
        BracketPrediction(
            player_id=player.id, category="nba_champion",
            predicted_value="Boston Celtics", is_correct=True, points_earned=10,
        )
    )
    db.session.commit()

    _login(client, player)
    resp = client.get("/classement")

    assert resp.status_code == 200
    assert b"11.0" in resp.data  # 1 (game) + 10 (bracket)
    assert b"Bob" in resp.data  # even players with 0 points are shown


# --- bracket -------------------------------------------------------------

def test_bracket_submission_when_unlocked(app, client, player):
    _login(client, player)
    resp = client.post("/bracket/", data={"nba_champion": "Boston Celtics"}, follow_redirects=True)

    assert resp.status_code == 200
    pred = BracketPrediction.query.filter_by(player_id=player.id, category="nba_champion").first()
    assert pred is not None
    assert pred.predicted_value == "Boston Celtics"


def test_bracket_locked_once_playoffs_started(app, client, player):
    series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()
    db.session.add(
        Game(series_id=series.id, team_a="Boston Celtics", team_b="Denver Nuggets", game_date=PAST, result="team_a")
    )
    db.session.commit()

    _login(client, player)
    resp = client.post("/bracket/", data={"nba_champion": "Boston Celtics"}, follow_redirects=True)

    assert resp.status_code == 200
    assert BracketPrediction.query.filter_by(player_id=player.id, category="nba_champion").first() is None


# --- player profile -------------------------------------------------------

def test_player_profile_shows_own_open_predictions(app, client, player):
    series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()
    game = Game(series_id=series.id, team_a="Boston Celtics", team_b="Denver Nuggets", game_date=FUTURE)
    db.session.add(game)
    db.session.commit()

    _login(client, player)
    client.post(f"/predict/game/{game.id}", data={"side": "team_a"}, follow_redirects=True)

    resp = client.get(f"/joueur/{player.id}")
    assert resp.status_code == 200
    assert b"Boston Celtics" in resp.data


def test_player_profile_hides_others_open_predictions(app, client, player):
    other = Player(name="Bob", access_code="bob-code")
    db.session.add(other)
    series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()
    game = Game(series_id=series.id, team_a="Boston Celtics", team_b="Denver Nuggets", game_date=FUTURE)
    db.session.add(game)
    db.session.commit()
    db.session.add(
        Prediction(
            player_id=other.id, game_id=game.id, prediction_type="game_winner", predicted_value="team_a",
        )
    )
    db.session.commit()

    _login(client, player)
    resp = client.get(f"/joueur/{other.id}")

    assert resp.status_code == 200
    assert "Pas encore révélé".encode("utf-8") in resp.data


def test_player_profile_reveals_others_predictions_once_locked(app, client, player):
    other = Player(name="Bob", access_code="bob-code")
    db.session.add(other)
    series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()
    game = Game(
        series_id=series.id, team_a="Boston Celtics", team_b="Denver Nuggets", game_date=PAST, result="team_a",
    )
    db.session.add(game)
    db.session.commit()
    db.session.add(
        Prediction(
            player_id=other.id, game_id=game.id, prediction_type="game_winner", predicted_value="team_a",
            is_correct=True, points_earned=1,
        )
    )
    db.session.commit()

    _login(client, player)
    resp = client.get(f"/joueur/{other.id}")

    assert resp.status_code == 200
    assert b"Boston Celtics" in resp.data


# --- ordering: most recent series/games first -----------------------------

def test_dashboard_orders_series_most_recent_first(app, client, player):
    """The oldest round (first_round) was created first (lower id), the
    finals last - but the dashboard should show the finals (latest games)
    on top, oldest round at the bottom."""
    old_series = Series(season=2025, round="first_round", team_a="Miami Heat", team_b="Orlando Magic")
    new_series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add_all([old_series, new_series])
    db.session.commit()
    db.session.add_all(
        [
            Game(
                series_id=old_series.id, team_a="Miami Heat", team_b="Orlando Magic",
                game_date=PAST - timedelta(days=30), result="team_a",
            ),
            Game(
                series_id=new_series.id, team_a="Boston Celtics", team_b="Denver Nuggets",
                game_date=PAST, result="team_a",
            ),
        ]
    )
    db.session.commit()

    _login(client, player)
    resp = client.get("/")

    body = resp.data.decode("utf-8")
    assert body.index("Boston Celtics") < body.index("Miami Heat")


def test_dashboard_orders_games_most_recent_first(app, client, player):
    series = Series(season=2025, round="finals", team_a="Boston Celtics", team_b="Denver Nuggets")
    db.session.add(series)
    db.session.commit()
    older_game = Game(
        series_id=series.id, team_a="Boston Celtics", team_b="Denver Nuggets",
        game_date=PAST - timedelta(days=5), result="team_a",
    )
    newer_game = Game(
        series_id=series.id, team_a="Boston Celtics", team_b="Denver Nuggets",
        game_date=PAST, result="team_b",
    )
    db.session.add_all([older_game, newer_game])
    db.session.commit()

    _login(client, player)
    resp = client.get("/")

    body = resp.data.decode("utf-8")
    assert body.index(newer_game.game_date.strftime("%d/%m")) < body.index(
        older_game.game_date.strftime("%d/%m")
    )
