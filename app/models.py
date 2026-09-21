"""Modèle de données SQLAlchemy, tel que défini dans la spec (voir section
"Data model" et "Pre-playoffs bracket predictions" du document de spec).

Deux petits ajouts par rapport au texte de la spec, nécessaires pour que le
schéma tienne debout - à valider avec Benoit :

- `Prediction.prediction_type` : la spec dit qu'une série peut recevoir deux
  pronostics distincts ("winner and exact score"), tous deux rattachés à
  `series_id`. Sans champ pour les distinguer, impossible de savoir lequel
  est lequel une fois en base -> ajout d'un type explicite
  (game_winner / series_winner / series_score).
- `Series.winner_odds` et `Series.score_odds` sont stockés en JSON plutôt
  qu'en simple nombre, car il y a une cote par équipe (winner_odds) et une
  cote par score exact possible, ex. 4-0, 4-1, 4-2, 4-3 (score_odds).
"""
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, UniqueConstraint

from app.extensions import db


def _utcnow():
    return datetime.now(timezone.utc)


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    # Lien ou code d'accès du joueur, tient lieu de login (pas de mot de passe, confirmé).
    access_code = db.Column(db.String(64), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(timezone=True), default=_utcnow, nullable=False)

    predictions = db.relationship("Prediction", back_populates="player", lazy="dynamic")
    bracket_predictions = db.relationship(
        "BracketPrediction", back_populates="player", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Player {self.id} {self.name!r}>"


class Series(db.Model):
    __tablename__ = "series"

    id = db.Column(db.Integer, primary_key=True)
    # année de DÉBUT de saison, convention balldontlie (ex: 2025 pour la
    # saison 2025-26, dont les playoffs se jouent en avril-juin 2026).
    # Nullable pour rester compatible avec les séries créées avant cet ajout -
    # mais à renseigner systématiquement pour toute nouvelle série, c'est ce
    # qui permet à l'ingestion de ne pas se tromper si les deux mêmes équipes
    # se recroisent une autre année.
    season = db.Column(db.Integer, nullable=True)
    # ex: "first_round", "conf_semis", "conf_finals", "finals"
    round = db.Column(db.String(32), nullable=False)
    team_a = db.Column(db.String(64), nullable=False)
    team_b = db.Column(db.String(64), nullable=False)

    # Cotes saisies manuellement par l'admin (Benoit), theoddsapi.com ne couvrant
    # pas les marchés vainqueur-de-série / score-de-série en offre gratuite.
    # winner_odds: {"team_a": 1.83, "team_b": 2.10}
    winner_odds = db.Column(db.JSON, nullable=True)
    # score_odds: {"4-0": 6.5, "4-1": 5.0, "4-2": 3.5, "4-3": 3.0} (clé = score de l'équipe gagnante-perdante)
    score_odds = db.Column(db.JSON, nullable=True)

    games = db.relationship("Game", back_populates="series", lazy="dynamic")
    predictions = db.relationship("Prediction", back_populates="series", lazy="dynamic")

    def __repr__(self):
        return f"<Series {self.id} {self.team_a} vs {self.team_b} ({self.round})>"


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id"), nullable=False)
    team_a = db.Column(db.String(64), nullable=False)
    team_b = db.Column(db.String(64), nullable=False)
    game_date = db.Column(db.DateTime(timezone=True), nullable=False)
    # "team_a" / "team_b" une fois le match joué, vide avant
    result = db.Column(db.String(16), nullable=True)
    # Cote moneyline, récupérée automatiquement via theoddsapi.com
    # ex: {"team_a": 1.65, "team_b": 2.25}
    game_odds = db.Column(db.JSON, nullable=True)
    # id du match côté balldontlie.io, pour ré-exécuter l'ingestion sans créer
    # de doublons (ajouté avec le script d'ingestion - voir sql/002_*.sql pour
    # une base déjà créée avant cet ajout).
    external_id = db.Column(db.String(32), unique=True, nullable=True)

    series = db.relationship("Series", back_populates="games")
    predictions = db.relationship("Prediction", back_populates="game", lazy="dynamic")

    def __repr__(self):
        return f"<Game {self.id} {self.team_a} vs {self.team_b} on {self.game_date}>"


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id"), nullable=True)

    # game_winner (game_id renseigné) / series_winner / series_score (series_id renseigné)
    prediction_type = db.Column(db.String(16), nullable=False)
    predicted_value = db.Column(db.String(32), nullable=False)  # ex: "team_a", "4-2"
    is_correct = db.Column(db.Boolean, nullable=True)
    points_earned = db.Column(db.Float, nullable=True, default=0)

    player = db.relationship("Player", back_populates="predictions")
    game = db.relationship("Game", back_populates="predictions")
    series = db.relationship("Series", back_populates="predictions")

    __table_args__ = (
        CheckConstraint(
            "(game_id IS NOT NULL AND series_id IS NULL) OR "
            "(game_id IS NULL AND series_id IS NOT NULL)",
            name="ck_prediction_game_xor_series",
        ),
        UniqueConstraint("player_id", "game_id", name="uq_prediction_player_game"),
        UniqueConstraint(
            "player_id", "series_id", "prediction_type", name="uq_prediction_player_series_type"
        ),
    )

    def __repr__(self):
        target = f"game={self.game_id}" if self.game_id else f"series={self.series_id}"
        return f"<Prediction {self.id} player={self.player_id} {target} -> {self.predicted_value}>"


class ScoringConfig(db.Model):
    """Valeurs de points, en base plutôt que codées en dur, modifiables sans toucher
    au code. Une ligne par règle, par moteur (classic / odds_based)."""

    __tablename__ = "scoring_config"

    id = db.Column(db.Integer, primary_key=True)
    engine = db.Column(db.String(16), nullable=False)  # "classic" | "odds_based"
    rule_key = db.Column(db.String(64), nullable=False)
    rule_value = db.Column(db.Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("engine", "rule_key", name="uq_scoring_config_engine_rule"),
    )

    def __repr__(self):
        return f"<ScoringConfig {self.engine}.{self.rule_key}={self.rule_value}>"


class BracketPrediction(db.Model):
    """Pronostics d'avant-playoffs (champion NBA, MVP des finales, champion de
    conférence Est/Ouest), verrouillés avant le premier match et notés une seule
    fois en fin de playoffs - table séparée des pronostics match/série."""

    __tablename__ = "bracket_predictions"

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=False)
    # "nba_champion" | "finals_mvp" | "east_champion" | "west_champion"
    category = db.Column(db.String(32), nullable=False)
    predicted_value = db.Column(db.String(64), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=True)
    points_earned = db.Column(db.Float, nullable=True, default=0)

    player = db.relationship("Player", back_populates="bracket_predictions")

    __table_args__ = (
        UniqueConstraint("player_id", "category", name="uq_bracket_prediction_player_category"),
    )

    def __repr__(self):
        return f"<BracketPrediction {self.id} player={self.player_id} {self.category}={self.predicted_value}>"
