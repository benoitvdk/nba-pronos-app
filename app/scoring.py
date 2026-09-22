"""Pure logic for the two scoring engines (see the "Scoring system" section
of the spec). No dependency on Flask/SQLAlchemy here: only functions that
take plain values as input and return (is_correct, points), so they can be
tested independently of the database (see tests/test_scoring.py). Wiring
to the database happens in app/scoring_service.py.
"""

ENGINES = ("classic", "odds_based")

# NBA Cup rounds (see app/models.py Series.round, app/ingestion.py
# sync_cup_games_from_balldontlie): group stage and every knockout round
# are single games, never a best-of-N series like the playoffs - every Cup
# round value uses this prefix so the rest of the app can tell the two
# competitions' rounds apart from the round string alone, with no separate
# "competition" column needed.
CUP_ROUND_PREFIX = "cup_"


def _check_engine(engine):
    if engine not in ENGINES:
        raise ValueError(f"unknown engine: {engine!r} (expected: {ENGINES})")


def is_cup_round(round_name):
    """True for any NBA Cup round (group stage or knockout)."""
    return round_name.startswith(CUP_ROUND_PREFIX)


def games_to_win_for_round(round_name):
    """Wins needed to decide a "series" for this round: 1 for any Cup
    round (a single game decides it), 4 (best-of-7) for a playoff round."""
    return 1 if is_cup_round(round_name) else 4


def series_status(wins_a, wins_b, games_to_win=4):
    """Computes a series' status from each team's win count (derived from
    games played). `score` follows the convention used in
    Series.score_odds: "winner's wins-loser's wins", e.g. "4-2"."""
    finished = wins_a >= games_to_win or wins_b >= games_to_win
    if wins_a >= games_to_win:
        winner, loser_wins = "team_a", wins_b
    elif wins_b >= games_to_win:
        winner, loser_wins = "team_b", wins_a
    else:
        winner, loser_wins = None, None
    score = f"{games_to_win}-{loser_wins}" if finished else None
    return {"wins_a": wins_a, "wins_b": wins_b, "finished": finished, "winner": winner, "score": score}


def score_game_winner(engine, cfg, predicted_team, actual_winner, odds=None):
    """predicted_team / actual_winner: "team_a" or "team_b".
    odds (odds_based engine): {"team_a": odds, "team_b": odds}, the odds of
    the predicted team used to multiply the points."""
    _check_engine(engine)
    is_correct = predicted_team == actual_winner
    if not is_correct:
        return False, 0.0
    if engine == "classic":
        return True, float(cfg["game_winner_points"])
    if not odds or predicted_team not in odds:
        raise ValueError("missing odds for the odds_based engine (game_odds)")
    return True, float(cfg["game_winner_points"]) * float(odds[predicted_team])


def score_series_winner(engine, cfg, predicted_team, actual_winner, winner_odds=None):
    _check_engine(engine)
    is_correct = predicted_team == actual_winner
    if not is_correct:
        return False, 0.0
    if engine == "classic":
        return True, float(cfg["series_winner_points"])
    if not winner_odds or predicted_team not in winner_odds:
        raise ValueError("missing odds for the odds_based engine (series.winner_odds)")
    return True, float(cfg["series_winner_points"]) * float(winner_odds[predicted_team])


def series_score_key(predicted_team, score):
    """Combines the predicted winning team and the exact score into a
    single value storable in Prediction.predicted_value, e.g. "team_b:4-2"."""
    return f"{predicted_team}:{score}"


def score_series_score(engine, cfg, predicted_score, actual_score, score_odds=None):
    """predicted_score / actual_score: e.g. "4-2"."""
    _check_engine(engine)
    is_correct = predicted_score == actual_score
    if not is_correct:
        return False, 0.0
    if engine == "classic":
        return True, float(cfg["series_score_bonus_points"])
    if not score_odds or predicted_score not in score_odds:
        raise ValueError("missing odds for the odds_based engine (series.score_odds)")
    return True, float(cfg["series_score_points"]) * float(score_odds[predicted_score])


def score_bracket(cfg_bracket, category, predicted_value, actual_value):
    """cfg_bracket: dict rule_key -> rule_value for the "bracket" engine
    (e.g. {"nba_champion_points": 10, ...}). No odds engine here: the spec
    only calls for a fixed point value per category for the bracket."""
    is_correct = predicted_value == actual_value
    if not is_correct:
        return False, 0.0
    key = f"{category}_points"
    if key not in cfg_bracket:
        raise ValueError(f"no point value for category {category!r} ({key} missing)")
    return True, float(cfg_bracket[key])
