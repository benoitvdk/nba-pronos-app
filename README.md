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

## Deploying to Render

Deploy via Blueprint (`render.yaml` at the repo root): on render.com,
*New +* → *Blueprint* → connect the GitHub repo → Render detects
`render.yaml` and proposes the `nba-playoffs-pronos` service. `SECRET_KEY`
is generated automatically; `DATABASE_URL`, `ODDS_API_KEY` and
`BALLDONTLIE_API_KEY` need to be filled in manually in the Render
dashboard (same values as in the local `.env`).

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
  config.py        config read from environment variables
  extensions.py    shared SQLAlchemy instance
  models.py        tables: players, series, games, predictions,
                    scoring_config, bracket_predictions
  auth.py          login via link/access code (no password)
  home.py          dashboard: open + already-submitted predictions
  predictions.py   prediction submission (game, series winner/score)
  leaderboard.py   leaderboard of all players
  bracket.py       "pre-playoffs" predictions (champion, MVP, etc.)
  time_utils.py    datetime normalization (SQLite vs Postgres)
  templates/       login.html, home.html, base.html, leaderboard.html,
                    bracket.html
  static/          manifest.json, sw.js, offline.html, icons/ (PWA)
  scoring.py       pure logic for the 2 scoring engines (testable alone)
  scoring_service.py  wires scoring.py to real data (DB)
  ingestion.py     turns API responses into up-to-date Game rows (testable alone)
  clients/         HTTP clients balldontlie.py and odds_api.py
scripts/
  init_db.py       creates the tables + seeds scoring_config
  add_player.py    adds a player and generates their login link
  run_scoring.py   recomputes points for game/series predictions
  score_bracket.py scores a bracket category once the result is known
  ingest.py        fetches results + odds and updates the database
sql/
  schema.sql, seed_scoring_config.sql, 002_add_external_id_to_games.sql,
  003_add_season_to_series.sql
tests/
  test_scoring.py    unit tests for the 2 scoring engines
  test_ingestion.py  ingestion tests (mocked APIs, no network calls)
  test_web.py        web route tests (predictions, leaderboard, bracket)
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
