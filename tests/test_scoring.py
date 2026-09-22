import pytest

from app.scoring import (
    games_to_win_for_round,
    is_cup_round,
    score_game_winner,
    score_series_winner,
    score_series_score,
    score_bracket,
    series_status,
)

CLASSIC_CFG = {
    "game_winner_points": 1,
    "series_winner_points": 1,
    "series_score_bonus_points": 3,
}
ODDS_CFG = {
    "game_winner_points": 1,
    "series_winner_points": 1,
    "series_score_points": 1,
}
BRACKET_CFG = {
    "nba_champion_points": 10,
    "finals_mvp_points": 5,
    "east_champion_points": 5,
    "west_champion_points": 5,
}


# --- game winner -------------------------------------------------------

def test_game_winner_classic_correct():
    correct, points = score_game_winner("classic", CLASSIC_CFG, "team_a", "team_a")
    assert correct is True
    assert points == 1


def test_game_winner_classic_incorrect():
    correct, points = score_game_winner("classic", CLASSIC_CFG, "team_a", "team_b")
    assert correct is False
    assert points == 0


def test_game_winner_odds_based_correct_uses_predicted_team_odds():
    odds = {"team_a": 1.8, "team_b": 2.2}
    correct, points = score_game_winner("odds_based", ODDS_CFG, "team_a", "team_a", odds=odds)
    assert correct is True
    assert points == pytest.approx(1.8)


def test_game_winner_odds_based_incorrect_scores_zero():
    odds = {"team_a": 1.8, "team_b": 2.2}
    correct, points = score_game_winner("odds_based", ODDS_CFG, "team_a", "team_b", odds=odds)
    assert correct is False
    assert points == 0


def test_game_winner_odds_based_missing_odds_raises():
    with pytest.raises(ValueError):
        score_game_winner("odds_based", ODDS_CFG, "team_a", "team_a", odds=None)


def test_unknown_engine_raises():
    with pytest.raises(ValueError):
        score_game_winner("magic", CLASSIC_CFG, "team_a", "team_a")


# --- series winner -------------------------------------------------------

def test_series_winner_classic():
    correct, points = score_series_winner("classic", CLASSIC_CFG, "team_b", "team_b")
    assert correct is True
    assert points == 1


def test_series_winner_odds_based():
    odds = {"team_a": 1.5, "team_b": 3.2}
    correct, points = score_series_winner(
        "odds_based", ODDS_CFG, "team_b", "team_b", winner_odds=odds
    )
    assert correct is True
    assert points == pytest.approx(3.2)


# --- series score ----------------------------------------------------------

def test_series_score_classic_bonus():
    correct, points = score_series_score("classic", CLASSIC_CFG, "4-2", "4-2")
    assert correct is True
    assert points == 3


def test_series_score_wrong_score():
    correct, points = score_series_score("classic", CLASSIC_CFG, "4-1", "4-2")
    assert correct is False
    assert points == 0


def test_series_score_odds_based():
    score_odds = {"4-0": 6.5, "4-1": 5.0, "4-2": 3.5, "4-3": 3.0}
    correct, points = score_series_score(
        "odds_based", ODDS_CFG, "4-2", "4-2", score_odds=score_odds
    )
    assert correct is True
    assert points == pytest.approx(3.5)


# --- bracket -----------------------------------------------------------

def test_bracket_correct():
    correct, points = score_bracket(BRACKET_CFG, "nba_champion", "Celtics", "Celtics")
    assert correct is True
    assert points == 10


def test_bracket_incorrect():
    correct, points = score_bracket(BRACKET_CFG, "nba_champion", "Celtics", "Nuggets")
    assert correct is False
    assert points == 0


def test_bracket_unknown_category_raises():
    with pytest.raises(ValueError):
        score_bracket(BRACKET_CFG, "sixth_man", "X", "X")


# --- series_status -------------------------------------------------------

def test_series_status_in_progress():
    status = series_status(wins_a=2, wins_b=1)
    assert status["finished"] is False
    assert status["winner"] is None
    assert status["score"] is None


def test_series_status_finished_team_a():
    status = series_status(wins_a=4, wins_b=2)
    assert status["finished"] is True
    assert status["winner"] == "team_a"
    assert status["score"] == "4-2"


def test_series_status_finished_sweep():
    status = series_status(wins_a=0, wins_b=4)
    assert status["finished"] is True
    assert status["winner"] == "team_b"
    assert status["score"] == "4-0"


# --- NBA Cup: is_cup_round / games_to_win_for_round -----------------------

@pytest.mark.parametrize(
    "round_name,expected",
    [
        ("cup_group", True),
        ("cup_quarterfinal", True),
        ("cup_semifinal", True),
        ("cup_final", True),
        ("first_round", False),
        ("conf_semis", False),
        ("finals", False),
    ],
)
def test_is_cup_round(round_name, expected):
    assert is_cup_round(round_name) is expected


def test_games_to_win_for_round_cup_is_single_game():
    assert games_to_win_for_round("cup_group") == 1
    assert games_to_win_for_round("cup_quarterfinal") == 1


def test_games_to_win_for_round_playoffs_is_best_of_seven():
    assert games_to_win_for_round("first_round") == 4
    assert games_to_win_for_round("finals") == 4


def test_series_status_cup_round_finished_after_one_game():
    # A Cup "series" is a single game: one win for either side finishes it.
    status = series_status(wins_a=1, wins_b=0, games_to_win=games_to_win_for_round("cup_quarterfinal"))
    assert status["finished"] is True
    assert status["winner"] == "team_a"
    assert status["score"] == "1-0"
