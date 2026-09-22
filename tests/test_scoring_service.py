"""Integration tests for app/scoring_service.py: wiring the pure scoring
logic (app/scoring.py) to real Game/Series/Prediction rows. Uses the Flask
test client's in-memory SQLite database, same setup as test_web.py."""
import os
from datetime import datetime, timedelta, timezone

import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret")

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models import Game, Player, Prediction, ScoringConfig, Series  # noqa: E402
from app.scoring_service import score_game_predictions, score_series_predictions  # noqa: E402

PAST = datetime.now(timezone.utc) - timedelta(days=1)


@pytest.fixture
def app():
    flask_app = create_app()
    flask_app.config.update(TESTING=True)
    with flask_app.app_context():
        db.create_all()
        for rule_key, rule_value in {
            "game_winner_points": 1,
            "series_winner_points": 1,
            "series_score_bonus_points": 3,
        }.items():
            db.session.add(ScoringConfig(engine="classic", rule_key=rule_key, rule_value=rule_value))
        db.session.commit()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def player(app):
    p = Player(name="Alice", access_code="alice-code")
    db.session.add(p)
    db.session.commit()
    return p


def _finished_series(team_a_wins, team_b_wins, **series_kwargs):
    series = Series(round="finals", team_a="Team A", team_b="Team B", **series_kwargs)
    db.session.add(series)
    db.session.flush()
    for i in range(team_a_wins):
        db.session.add(Game(series_id=series.id, team_a="Team A", team_b="Team B", game_date=PAST, result="team_a"))
    for i in range(team_b_wins):
        db.session.add(Game(series_id=series.id, team_a="Team A", team_b="Team B", game_date=PAST, result="team_b"))
    db.session.commit()
    return series


def test_score_game_predictions_marks_correct_and_wrong(app, player):
    game = Game(series_id=_finished_series(4, 0).id, team_a="Team A", team_b="Team B", game_date=PAST, result="team_a")
    db.session.add(game)
    db.session.commit()
    correct = Prediction(player_id=player.id, game_id=game.id, prediction_type="game_winner", predicted_value="team_a")
    # second player, needed for the "wrong" prediction (unique player+game constraint)
    bob = Player(name="Bob", access_code="bob-code")
    db.session.add(bob)
    db.session.flush()
    wrong = Prediction(player_id=bob.id, game_id=game.id, prediction_type="game_winner", predicted_value="team_b")
    db.session.add_all([correct, wrong])
    db.session.commit()

    score_game_predictions(engine="classic")

    assert correct.is_correct is True
    assert correct.points_earned == 1
    assert wrong.is_correct is False
    assert wrong.points_earned == 0


def test_score_series_score_requires_matching_team_and_score(app, player):
    # Team A wins 4-2 - the actual outcome the two predictions below are compared against.
    series = _finished_series(4, 2)

    right_team_and_score = Prediction(
        player_id=player.id, series_id=series.id, prediction_type="series_score", predicted_value="team_a:4-2"
    )
    bob = Player(name="Bob", access_code="bob-code")
    db.session.add(bob)
    db.session.flush()
    # Same 4-2 score, but predicting the WRONG team as winner - must not be
    # scored as correct just because the score digits match (this was the
    # bug: predicted_value, e.g. "team_b:4-2", was compared as-is against
    # the bare score "4-2" from series_status, which is never equal, so
    # this used to score every series_score prediction as wrong; fixing
    # that naively (comparing only the score part) would instead make this
    # wrong-team case score as correct).
    right_score_wrong_team = Prediction(
        player_id=bob.id, series_id=series.id, prediction_type="series_score", predicted_value="team_b:4-2"
    )
    db.session.add_all([right_team_and_score, right_score_wrong_team])
    db.session.commit()

    score_series_predictions(engine="classic")

    assert right_team_and_score.is_correct is True
    assert right_team_and_score.points_earned == 3
    assert right_score_wrong_team.is_correct is False
    assert right_score_wrong_team.points_earned == 0


def test_score_series_winner(app, player):
    series = _finished_series(4, 1)
    pred = Prediction(player_id=player.id, series_id=series.id, prediction_type="series_winner", predicted_value="team_a")
    db.session.add(pred)
    db.session.commit()

    score_series_predictions(engine="classic")

    assert pred.is_correct is True
    assert pred.points_earned == 1


# --- NBA Cup: single-game "series" -----------------------------------------

def test_score_game_predictions_works_for_a_cup_round(app, player):
    """Cup rounds only ever carry game_winner predictions (see
    app/bracket.py, app/ingestion.py.sync_cup_games_from_balldontlie) - this
    is the same code path as a playoff game, just under a "cup_group"
    round, so it should score exactly the same way."""
    series = Series(round="cup_group", team_a="Team A", team_b="Team B", group_name="Groupe A (Est)")
    db.session.add(series)
    db.session.flush()
    game = Game(series_id=series.id, team_a="Team A", team_b="Team B", game_date=PAST, result="team_a")
    db.session.add(game)
    db.session.commit()
    pred = Prediction(player_id=player.id, game_id=game.id, prediction_type="game_winner", predicted_value="team_a")
    db.session.add(pred)
    db.session.commit()

    score_game_predictions(engine="classic")

    assert pred.is_correct is True
    assert pred.points_earned == 1


def test_score_series_predictions_treats_a_cup_series_as_finished_after_one_game(app, player):
    """A Cup round's "series" (see games_to_win_for_round) is finished the
    moment its single game has a result - it never carries a
    series_winner/series_score prediction in practice, so this just checks
    the finished-series loop doesn't choke on it and scores 0 predictions."""
    series = Series(round="cup_quarterfinal", team_a="Team A", team_b="Team B")
    db.session.add(series)
    db.session.flush()
    db.session.add(Game(series_id=series.id, team_a="Team A", team_b="Team B", game_date=PAST, result="team_a"))
    db.session.commit()

    updated = score_series_predictions(engine="classic")

    assert updated == 0
