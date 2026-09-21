"""Branche la logique pure de app/scoring.py aux données réelles (games,
series, predictions). Recalcule is_correct/points_earned pour tout ce qui
est déjà déterminable, à chaque exécution (idempotent - relancer ne fait
que rafraîchir les valeurs)."""
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
        raise ValueError(f"aucune ligne scoring_config pour l'engine {engine!r}")
    return {r.rule_key: r.rule_value for r in rows}


def _series_status(series):
    wins_a = sum(1 for g in series.games if g.result == "team_a")
    wins_b = sum(1 for g in series.games if g.result == "team_b")
    return series_status(wins_a, wins_b)


def score_game_predictions(engine="classic"):
    """Note les pronostics match par match dont le match a un résultat."""
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
    """Note les pronostics vainqueur-de-série et score-de-série pour les
    séries terminées."""
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
                is_correct, points = score_series_score(
                    engine, cfg, pred.predicted_value, status["score"], score_odds=series.score_odds
                )
            else:
                continue
            pred.is_correct = is_correct
            pred.points_earned = points
            updated += 1
    db.session.commit()
    return updated


def score_bracket_predictions(category, actual_value):
    """Note tous les pronostics bracket d'une catégorie une fois le résultat
    réel connu (saisi à la main par l'admin, ex. le champion NBA en fin de
    playoffs) - voir scripts/score_bracket.py."""
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
