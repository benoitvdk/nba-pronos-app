"""Logique pure des deux moteurs de scoring (voir section "Scoring system" de
la spec). Aucune dépendance à Flask/SQLAlchemy ici : uniquement des fonctions
qui prennent des valeurs simples en entrée et renvoient (is_correct, points),
pour pouvoir les tester indépendamment de la base (voir tests/test_scoring.py).
Le branchement à la base se fait dans app/scoring_service.py.
"""

ENGINES = ("classic", "odds_based")


def _check_engine(engine):
    if engine not in ENGINES:
        raise ValueError(f"moteur inconnu : {engine!r} (attendu : {ENGINES})")


def series_status(wins_a, wins_b, games_to_win=4):
    """Calcule l'état d'une série à partir du nombre de victoires de chaque
    équipe (déduit des games jouées). `score` reprend la convention utilisée
    dans Series.score_odds : "victoires du vainqueur-victoires du perdant",
    ex. "4-2"."""
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
    """predicted_team / actual_winner : "team_a" ou "team_b".
    odds (moteur odds_based) : {"team_a": cote, "team_b": cote}, cote de
    l'équipe pronostiquée utilisée pour multiplier les points."""
    _check_engine(engine)
    is_correct = predicted_team == actual_winner
    if not is_correct:
        return False, 0.0
    if engine == "classic":
        return True, float(cfg["game_winner_points"])
    if not odds or predicted_team not in odds:
        raise ValueError("cote manquante pour le moteur odds_based (game_odds)")
    return True, float(cfg["game_winner_points"]) * float(odds[predicted_team])


def score_series_winner(engine, cfg, predicted_team, actual_winner, winner_odds=None):
    _check_engine(engine)
    is_correct = predicted_team == actual_winner
    if not is_correct:
        return False, 0.0
    if engine == "classic":
        return True, float(cfg["series_winner_points"])
    if not winner_odds or predicted_team not in winner_odds:
        raise ValueError("cote manquante pour le moteur odds_based (series.winner_odds)")
    return True, float(cfg["series_winner_points"]) * float(winner_odds[predicted_team])


def series_score_key(predicted_team, score):
    """Combine l'équipe pronostiquée gagnante et le score exact en une seule
    valeur stockable dans Prediction.predicted_value, ex. "team_b:4-2"."""
    return f"{predicted_team}:{score}"


def score_series_score(engine, cfg, predicted_score, actual_score, score_odds=None):
    """predicted_score / actual_score : ex. "4-2"."""
    _check_engine(engine)
    is_correct = predicted_score == actual_score
    if not is_correct:
        return False, 0.0
    if engine == "classic":
        return True, float(cfg["series_score_bonus_points"])
    if not score_odds or predicted_score not in score_odds:
        raise ValueError("cote manquante pour le moteur odds_based (series.score_odds)")
    return True, float(cfg["series_score_points"]) * float(score_odds[predicted_score])


def score_bracket(cfg_bracket, category, predicted_value, actual_value):
    """cfg_bracket : dict rule_key -> rule_value pour l'engine "bracket"
    (ex. {"nba_champion_points": 10, ...}). Pas de moteur cotes ici : la
    spec ne prévoit qu'un barème fixe par catégorie pour le bracket."""
    is_correct = predicted_value == actual_value
    if not is_correct:
        return False, 0.0
    key = f"{category}_points"
    if key not in cfg_bracket:
        raise ValueError(f"pas de barème pour la catégorie {category!r} ({key} manquant)")
    return True, float(cfg_bracket[key])
