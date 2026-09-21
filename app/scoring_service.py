"""Wires the pure logic from app/scoring.py to the real data (games,
series, predictions). Recomputes is_correct/points_earned for everything
that's already determinable, on every run (idempotent - re-running only
refreshes the values)."""
from app.extensions import db
from app.models import BracketPrediction, Game, Prediction, ScoringConfig, Series
from app.scoring import (
    score_bracket,
    score_game_winner,
    score_series_score,
    score_series_winner,
    series_status,
)


def load_config(engine):
    rows = ScoringConfig.query.filter_by(engine=engine).all()
    if not rows:
        raise ValueError(f"no scoring_config row for engine {engine!r}")
    return {r.rule_key: r.rule_value for r in rows}


def _series_status(series):
    wins_a = sum(1 for g in series.games if g.result == "team_a")
    wins_b = sum(1 for g in series.games if g.result == "team_b")
    return series_status(wins_a, wins_b)


def score_game_predictions(engine="classic"):
    """Scores game-by-game predictions for games that have a result."""
    cfg = load_config(engine)
    updated = 0
    predictions = (
        Prediction.query.filter_by(prediction_type="game_winner")
        .join(Game, Prediction.game_id == Game.id)
        .filter(Game.result.isnot(None))
        .all()
    )
    for pred in predictions:
        is_correct, points = score_game_winner(
            engine, cfg, pred.predicted_value, pred.game.result, odds=pred.game.game_odds
        )
        pred.is_correct = is_correct
        pred.points_earned = points
        updated += 1
    db.session.commit()
    return updated


def score_series_predictions(engine="classic"):
    """Scores series-winner and series-score predictions for finished
    series."""
    cfg = load_config(engine)
    updated = 0
    for series in Series.query.all():
        status = _series_status(series)
        if not status["finished"]:
            continue
        for pred in series.predictions:
            if pred.prediction_type == "series_winner":
                is_correct, points = score_series_winner(
                    engine, cfg, pred.predicted_value, status["winner"], winner_odds=series.winner_odds
                )
            elif pred.prediction_type == "series_score":
                # predicted_value combines team + score (e.g. "team_b:4-2",
                # see series_score_key) but status["score"] is only the
                # number part (e.g. "4-2") - split it back out before
                # comparing, and the team must match too, otherwise a
                # right score for the wrong team would score as correct.
                predicted_team, _, predicted_score = pred.predicted_value.partition(":")
                is_correct, points = score_series_score(
                    engine, cfg, predicted_score, status["score"], score_odds=series.score_odds
                )
                if predicted_team != status["winner"]:
                    is_correct, points = False, 0.0
            else:
                continue
            pred.is_correct = is_correct
            pred.points_earned = points
            updated += 1
    db.session.commit()
    return updated


def score_bracket_predictions(category, actual_value):
    """Scores every bracket prediction for a category once the real result
    is known (entered by hand by the admin, e.g. the NBA champion at the
    end of the playoffs) - see scripts/score_bracket.py."""
    cfg_bracket = load_config("bracket")
    updated = 0
    predictions = BracketPrediction.query.filter_by(category=category).all()
    for pred in predictions:
        is_correct, points = score_bracket(cfg_bracket, category, pred.predicted_value, actual_value)
        pred.is_correct = is_correct
        pred.points_earned = points
        updated += 1
    db.session.commit()
    return updated
