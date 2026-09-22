# NBA Playoffs Pronos App

App for predicting NBA playoff game outcomes (in the style of Mon Petit
Pronostic), built in Python, 100% free to host. See `Spec App Pronostics
Playoffs NBA.md` for the full spec.

## Stack

- Backend: Flask, deployed on Render (free tier)
- Database: Neon (free Postgres)
- ORM: Flask-SQLAlchemy

## Local setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env: fill in DATABASE_URL (Neon) and SECRET_KEY

python -m scripts.init_db   # creates the tables + seeds scoring_config
python -m scripts.add_player "First Last"   # creates a player + their login link
python wsgi.py              # starts the dev server on http://127.0.0.1:5000
```

To run the tests (scoring logic, independent of the database):

```bash
pip install -r requirements-dev.txt
pytest
```

To recompute points once game results are in the database:

```bash
python -m scripts.run_scoring --engine classic      # or --engine odds_based
python -m scripts.score_bracket --category nba_champion --winner "Boston Celtics"
```

## Automatic ingestion (results + odds)

Ingestion (`scripts/ingest.py`) only updates games for series that already
exist: **each `Series` must be created by hand first** (season, round,
team_a, team_b — and if you want the odds-based engine, `winner_odds` /
`score_odds`) via Neon's SQL Editor, for example:

```sql
INSERT INTO series (season, round, team_a, team_b)
VALUES (2025, 'finals', 'New York Knicks', 'San Antonio Spurs');
```

Team names must be written exactly as in balldontlie/theoddsapi (full
name, e.g. "Boston Celtics", not "BOS"). `season` follows the balldontlie
convention: the **starting** year of the season (e.g. 2025 for the 2026
NBA finals, played in June 2026 at the end of the 2025-26 season) —
always fill it in, since that's what prevents confusion if the same two
teams meet again in another year.

If your database was created before these additions, first run
`sql/002_add_external_id_to_games.sql` then
`sql/003_add_season_to_series.sql` in Neon's SQL Editor (a fresh database
created via `init_db.py` already has both columns).

You'll also need a free balldontlie.io API key (Sign Up on balldontlie.io,
Free tier, 5 req/min) to add to `.env` (`BALLDONTLIE_API_KEY`).

```bash
python -m scripts.ingest --season 2025   # test: 2026 finals (Knicks-Spurs, already played)
python -m scripts.ingest --season 2026   # real 2027 playoffs, once they start
```

A GitHub Actions workflow (`.github/workflows/ingest.yml`) is ready to run
this automatically every hour, for free, on a public repo — you just need
to add `DATABASE_URL`, `BALLDONTLIE_API_KEY` and `ODDS_API_KEY` to the
GitHub repo secrets (Settings > Secrets and variables > Actions), and
update `--season` in there when the time comes.

Known limitation: theoddsapi.com only provides odds for upcoming/live
games (no history on the free tier), so the odds part can only really be
tested once the 2026 playoffs start.

`/health` responds `{"status": "ok"}` once the server is running. The link
shown by `add_player` (e.g. `http://127.0.0.1:5000/login/<code>`) logs in
directly, no password.

## NBA Cup mode

The app can also run the NBA Cup (in-season tournament) instead of the
playoffs - never both at the same time. Which one is live is controlled by
the `APP_MODE` environment variable (`playoffs` or `nba_cup`, default
`playoffs`): it switches the labels shown everywhere (title, nav, bracket
page) and which `Series`/`Game` rows show up on the dashboard and
leaderboard. Switching modes is just changing `APP_MODE` (`.env` locally,
the Render dashboard in production) and redeploying - the same database
can be reused across a season (Cup in November-December, then playoffs in
April), predictions and points from one mode never leak into the other's
leaderboard.

The two competitions are modeled differently under the hood, because a Cup
round is always a single game (round-robin group stage, then
single-elimination knockout) rather than a best-of-7 series:

- A Cup matchup is still stored as a `Series` row (to reuse the whole
  prediction/scoring pipeline), tagged via `round` with a `cup_` prefix
  (`cup_group`, `cup_quarterfinal`, `cup_semifinal`, `cup_final`) - but
  it's always a "series" of exactly one game.
- Unlike the playoffs, **you don't need to create these series by hand**:
  `scripts/ingest.py --season-type ist` creates them automatically, the
  first time it sees a given pairing, reading both the round (group stage
  or which knockout round) AND the exact group straight off balldontlie's
  `ist_stage` field (confirmed against their docs - null for regular
  season/playoff games, one of `East/West Group A/B/C`,
  `East/West Quarterfinal`, `East/West Semifinal`, `Championship` for a
  Cup game). Nothing to configure - same command shape as the playoffs:

  ```bash
  python -m scripts.ingest --season 2026 --season-type ist
  ```

- Only game-winner predictions exist for a Cup round (no series
  winner/exact-score prediction - meaningless for a single game); the
  dashboard hides that section automatically for a Cup round.
- Pre-Cup bonus predictions (`/bracket/`) become: NBA Cup champion,
  Eastern/Western finalist, and the 6 group winners, instead of the
  playoffs' champion/MVP/conference-champion categories (see
  `app/bracket.py` `CUP_CATEGORIES` - provisional point values in
  `scripts/init_db.py` / `sql/seed_scoring_config.sql`, adjust as needed).
- `.github/workflows/ingest.yml` runs a fixed command - update its `Run
  ingestion` step (add `--season-type ist`) when switching to Cup mode,
  and back when switching to playoffs.
- If your database was created before this addition, also run
  `sql/004_add_group_name_to_series.sql` in Neon's SQL Editor (a fresh
  database via `init_db.py` already has the column).

## Deploying to Render

Deploy via Blueprint (`render.yaml` at the repo root): on render.com,
*New +* → *Blueprint* → connect the GitHub repo → Render detects
`render.yaml` and proposes the `nba-playoffs-pronos` service. `SECRET_KEY`
is generated automatically; `DATABASE_URL`, `ODDS_API_KEY` and
`BALLDONTLIE_API_KEY` need to be filled in manually in the Render
dashboard (same values as in the local `.env`). `APP_MODE` defaults to
`playoffs` in `render.yaml` - switch it to `nba_cup` in the Render
dashboard (see "NBA Cup mode" above) when it's time, no code change
needed.

Render's free plan puts the service to sleep after 15 minutes of
inactivity (30 to 60 seconds wake-up on the next load). For the GitHub
Actions ingestion cron to work, add the same 3 secrets (`DATABASE_URL`,
`BALLDONTLIE_API_KEY`, `ODDS_API_KEY`) to the GitHub repo's Actions
secrets (not the variables).

## Usage (frontend)

Once logged in via their link, each player lands on `/` (dashboard):

- for each series: prediction for the series winner + exact score (team +
  combined score, e.g. "Celtics win 4-2"), and for each upcoming game a
  prediction for the game winner. Everything stays editable until tip-off
  (game) or until the first game of the series has been played
  (series winner/score), then locks.
- `/classement`: leaderboard of all players (game/series predictions +
  bracket combined), including those with 0 points.
- `/bracket/`: "pre-playoffs" predictions (NBA champion, Finals MVP,
  Eastern/Western champion) — free text, locked as soon as the first
  playoff game has been played.

Each series on `/` is a collapsible card (finished series start collapsed,
the current/upcoming ones start open), so the dashboard stays quick to
render once a full playoffs' worth of series have piled up. Manually
opening or closing a series is remembered per browser (`localStorage`),
independently of the default.

The app is an installable PWA (manifest + service worker, generated
icons): on mobile or desktop, the browser offers "Install app" / "Add to
Home Screen". An offline page is shown if the player loses their
connection. The service worker is served from `/sw.js` (not
`/static/sw.js`) on purpose, so its scope covers the whole app rather
than just `/static/`.

## Structure

```
app/
  __init__.py      Flask application factory
  config.py        config read from environment variables (incl. APP_MODE)
  extensions.py    shared SQLAlchemy instance
  models.py        tables: players, series (+ group_name for the Cup),
                    games, predictions, scoring_config, bracket_predictions
  auth.py          login via link/access code (no password)
  home.py          dashboard: open + already-submitted predictions
  predictions.py   prediction submission (game, series winner/score)
  leaderboard.py   leaderboard of all players, scoped to the current mode
  bracket.py       pre-tournament predictions - categories depend on
                    APP_MODE (champion/MVP/conf. champions, or Cup
                    champion/finalists/group winners)
  time_utils.py    datetime normalization (SQLite vs Postgres)
  templates/       login.html, home.html, base.html, leaderboard.html,
                    bracket.html
  static/          manifest.json, sw.js, offline.html, icons/ (PWA)
  scoring.py       pure logic for the 2 scoring engines, + is_cup_round /
                    games_to_win_for_round (testable alone)
  scoring_service.py  wires scoring.py to real data (DB)
  ingestion.py     turns API responses into up-to-date Game rows - playoffs
                    (series must exist) and NBA Cup (series auto-created),
                    testable alone
  clients/         HTTP clients balldontlie.py and odds_api.py
scripts/
  init_db.py       creates the tables + seeds scoring_config
  add_player.py    adds a player and generates their login link
  run_scoring.py   recomputes points for game/series predictions
  score_bracket.py scores a bracket category once the result is known
  ingest.py        fetches results + odds and updates the database
                    (--season-type ist --stage ... for the Cup)
sql/
  schema.sql, seed_scoring_config.sql, 002_add_external_id_to_games.sql,
  003_add_season_to_series.sql, 004_add_group_name_to_series.sql
tests/
  test_scoring.py    unit tests for the 2 scoring engines + Cup helpers
  test_ingestion.py  ingestion tests (mocked APIs, no network calls),
                    playoffs and Cup
  test_web.py        web route tests (predictions, leaderboard, bracket),
                    playoffs and Cup mode
.github/workflows/
  ingest.yml       GitHub Actions cron (free) for automatic ingestion
render.yaml        Render Blueprint (web service + environment variables)
wsgi.py            entry point for gunicorn / Render
```

## Progress

- [x] Data model
- [x] Simple authentication via player link/code
- [x] Scoring engines (classic + odds-based)
- [x] Automatic ingestion script (results + odds)
- [x] PWA frontend (predictions, leaderboard, bracket, installable, offline)
- [x] Deployed on Render
- [ ] Clean up test series before the real 2026-27 season
- [ ] Average odds across multiple bookmakers instead of only taking the
      first one available (`app/ingestion.py`, `sync_odds_from_oddsapi`)
- [x] Support the NBA Cup as an alternate mode (`APP_MODE=nba_cup`, never
      at the same time as the playoffs - see "NBA Cup mode" above) - built
      on `feature/nba-cup`, not yet run against the real 2026-27 Cup
