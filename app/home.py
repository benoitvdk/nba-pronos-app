"""Dashboard: games and series still open for prediction for the logged-in
player, plus what they've already predicted. Once a game or series is
locked (tip-off passed / series started), every player's predictions for
that item become visible to any logged-in player - never before, so as
not to influence other players' predictions.

Performance note: this route used to issue one or two extra SQL queries
per game and per series (own prediction + "everyone's predictions" once
locked), on top of fetching each series' games twice (once through the
`any(...)` "started" check on the lazy="dynamic" relationship, once
through the explicit ordered `.all()` used for display). At a realistic
scale (~24 players, mid-playoffs) that added up to 200+ sequential round
trips to the database for a single page load - fine on localhost, but
slow enough against a remote free-tier Postgres (Neon) to make the page
look like it "doesn't load" on Render. It's now 3 queries total,
independent of how many players/series/games exist."""
from collections import defaultdict
from datetime import datetime, timezone

from flask import Blueprint, g, render_template

from app.auth import login_required
from app.models import Game, Player, Prediction, Series
from app.predictions import VALID_SCORES
from app.scoring import series_status
from app.time_utils import ensure_aware_utc

bp = Blueprint("home", __name__)


def _other_prediction_entry(pred):
    return {"player_name": pred.player.name, "predicted_value": pred.predicted_value, "is_correct": pred.is_correct}


@bp.route("/")
@login_required
def index():
    now = datetime.now(timezone.utc)
    player = g.player

    series_list = Series.ordered_recent_first().all()
    series_ids = [series.id for series in series_list]

    # Query 1: every game for every series in one go (most recent first, so
    # each series' games list comes out already sorted like before).
    games_by_series = defaultdict(list)
    for game in Game.query.filter(Game.series_id.in_(series_ids)).order_by(Game.game_date.desc()).all():
        games_by_series[game.series_id].append(game)

    # Query 2: this player's own predictions, all at once.
    own_by_game = {}
    own_by_series = {}
    for pred in Prediction.query.filter_by(player_id=player.id).all():
        if pred.game_id is not None:
            own_by_game[pred.game_id] = pred
        else:
            own_by_series[(pred.series_id, pred.prediction_type)] = pred

    # Query 3 (with a join for player names): every OTHER player's
    # predictions, all at once - only the locked ones get shown in the
    # template, but fetching them all up front is one round trip instead of
    # one per locked game/series.
    other_by_game = defaultdict(list)
    other_by_series = defaultdict(list)
    other_predictions = (
        Prediction.query.filter(Prediction.player_id != player.id)
        .join(Player)
        .order_by(Player.name)
        .all()
    )
    for pred in other_predictions:
        entry = _other_prediction_entry(pred)
        if pred.game_id is not None:
            other_by_game[pred.game_id].append(entry)
        else:
            other_by_series[(pred.series_id, pred.prediction_type)].append(entry)

    series_rows = []
    for series in series_list:
        series_games = games_by_series.get(series.id, [])
        started = any(gm.result is not None for gm in series_games)
        wins_a = sum(1 for gm in series_games if gm.result == "team_a")
        wins_b = sum(1 for gm in series_games if gm.result == "team_b")
        status = series_status(wins_a, wins_b)

        winner_pred = own_by_series.get((series.id, "series_winner"))
        score_pred = own_by_series.get((series.id, "series_score"))

        # 1-indexed position of each game within the series in chronological
        # order (Game 1 .. Game 7), independent of series_games' own display
        # order (most recent first, see the query above).
        game_numbers = {
            gm.id: n for n, gm in enumerate(sorted(series_games, key=lambda gm: gm.game_date), start=1)
        }

        games_rows = []
        for game in series_games:
            open_ = game.result is None and ensure_aware_utc(game.game_date) > now
            games_rows.append(
                {
                    "game": game,
                    "game_number": game_numbers[game.id],
                    "prediction": own_by_game.get(game.id),
                    "open": open_,
                    "all_predictions": other_by_game.get(game.id, []) if not open_ else [],
                }
            )

        # Own running point total for this series (games + winner + score),
        # shown on the collapsed card header - own predictions are never
        # hidden from their author, so nothing to gate here.
        total_points = sum(
            float(gr["prediction"].points_earned or 0) for gr in games_rows if gr["prediction"]
        )
        if winner_pred:
            total_points += float(winner_pred.points_earned or 0)
        if score_pred:
            total_points += float(score_pred.points_earned or 0)

        series_rows.append(
            {
                "series": series,
                "started": started,
                "finished": status["finished"],
                "games": games_rows,
                "winner_prediction": winner_pred,
                "score_prediction": score_pred,
                "total_points": total_points,
                "all_winner_predictions": (
                    other_by_series.get((series.id, "series_winner"), []) if started else []
                ),
                "all_score_predictions": (
                    other_by_series.get((series.id, "series_score"), []) if started else []
                ),
            }
        )

    return render_template(
        "home.html", player=player, series_rows=series_rows, valid_scores=VALID_SCORES
    )
