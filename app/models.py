"""SQLAlchemy data model, as defined in the spec (see the "Data model" and
"Pre-playoffs bracket predictions" sections of the spec document).

Two small additions compared to the spec text, needed for the schema to
hold together - to confirm with Benoit:

- `Prediction.prediction_type`: the spec says a series can receive two
  distinct predictions ("winner and exact score"), both attached to
  `series_id`. Without a field to tell them apart, there's no way to know
  which is which once in the database -> added an explicit type
  (game_winner / series_winner / series_score).
- `Series.winner_odds` and `Series.score_odds` are stored as JSON rather
  than a plain number, since there's one odds value per team (winner_odds)
  and one per possible exact score, e.g. 4-0, 4-1, 4-2, 4-3 (score_odds).

NBA Cup addition - to confirm with Benoit: the app never runs the playoffs
and the Cup at the same time (see APP_MODE in app/config.py), so rather
than a whole parallel set of tables, a Cup group-stage or knockout matchup
is just another `Series` row, tagged via `round` (values prefixed "cup_",
see app/scoring.py CUP_ROUND_PREFIX) - always a "series" of exactly one
game, since the Cup never has a best-of-N round. `Series.group_name` is
only ever set for the group stage, to remember which of the 6 groups a
matchup belongs to (see app/ingestion.py sync_cup_games_from_balldontlie).
"""
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, UniqueConstraint, func

from app.extensions import db


def _utcnow():
    return datetime.now(timezone.utc)


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    # Player's access link/code, doubles as login (no password, confirmed).
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
    # STARTING year of the season, balldontlie convention (e.g. 2025 for
    # the 2025-26 season, whose playoffs are played in April-June 2026).
    # Nullable to stay compatible with series created before this field was
    # added - but should always be filled in for any new series, since
    # that's what lets ingestion avoid mistakes if the same two teams meet
    # again in another year.
    season = db.Column(db.Integer, nullable=True)
    # e.g.: "first_round", "conf_semis", "conf_finals", "finals"
    round = db.Column(db.String(32), nullable=False)
    team_a = db.Column(db.String(64), nullable=False)
    team_b = db.Column(db.String(64), nullable=False)

    # Odds entered manually by the admin (Benoit), since theoddsapi.com
    # doesn't cover series-winner / series-score markets on the free tier.
    # winner_odds: {"team_a": 1.83, "team_b": 2.10}
    winner_odds = db.Column(db.JSON, nullable=True)
    # score_odds: {"4-0": 6.5, "4-1": 5.0, "4-2": 3.5, "4-3": 3.0} (key = winning team-losing team score)
    score_odds = db.Column(db.JSON, nullable=True)
    # NBA Cup group stage only (round == "cup_group"), e.g. "Groupe A (Est)" -
    # always NULL for a playoff series or a Cup knockout round.
    group_name = db.Column(db.String(64), nullable=True)

    games = db.relationship("Game", back_populates="series", lazy="dynamic")
    predictions = db.relationship("Prediction", back_populates="series", lazy="dynamic")

    def __repr__(self):
        return f"<Series {self.id} {self.team_a} vs {self.team_b} ({self.round})>"

    @classmethod
    def ordered_recent_first(cls):
        """All series, most recently active first (based on the latest of
        their games' game_date), so the dashboard/profile pages read like a
        news feed: current round on top, older rounds further down. A
        series with no games yet (just created, nothing scheduled) sorts
        as if it were the most recent, since it's presumably the next
        thing to happen."""
        latest_game_date = (
            db.session.query(func.max(Game.game_date))
            .filter(Game.series_id == cls.id)
            .correlate(cls)
            .scalar_subquery()
        )
        far_future = datetime(2999, 1, 1, tzinfo=timezone.utc)
        return cls.query.order_by(func.coalesce(latest_game_date, far_future).desc())


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id"), nullable=False)
    team_a = db.Column(db.String(64), nullable=False)
    team_b = db.Column(db.String(64), nullable=False)
    game_date = db.Column(db.DateTime(timezone=True), nullable=False)
    # "team_a" / "team_b" once the game has been played, empty before
    result = db.Column(db.String(16), nullable=True)
    # Moneyline odds, fetched automatically via theoddsapi.com
    # e.g.: {"team_a": 1.65, "team_b": 2.25}
    game_odds = db.Column(db.JSON, nullable=True)
    # balldontlie.io game id, to re-run ingestion without creating
    # duplicates (added along with the ingestion script - see sql/002_*.sql
    # for a database created before this addition).
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

    # game_winner (game_id set) / series_winner / series_score (series_id set)
    prediction_type = db.Column(db.String(16), nullable=False)
    predicted_value = db.Column(db.String(32), nullable=False)  # e.g.: "team_a", "4-2"
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
    """Point values, kept in the database rather than hardcoded, so they can
    be changed without touching the code. One row per rule, per engine
    (classic / odds_based)."""

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
    """Pre-playoffs predictions (NBA champion, Finals MVP, Eastern/Western
    conference champion), locked before the first game and scored once at
    the end of the playoffs - table kept separate from game/series
    predictions."""

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
