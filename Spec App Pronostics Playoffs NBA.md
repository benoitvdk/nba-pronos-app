# NBA Playoffs Prediction App Spec

2026-09-17 · @Someone

## Overview and constraints

Mobile app for predicting NBA playoff game outcomes, inspired by Mon Petit Pronostic, built in Python and shipped as a PWA (progressive web app).

- Scope: NBA playoffs only, not the regular season
- Concept: predictions on game outcomes, no fantasy roster management
- Granularity: game-by-game predictions, plus series predictions (winner and exact score)
- Target group: 20-plus players
- Main constraint: entirely free solution (hosting, database, API), no credit card required
- Automatic retrieval of game results via an NBA API (nba\_api or balldontlie)
- Automatic retrieval of game odds via theoddsapi.com

## Technical stack (100 percent free)

| Component | Solution | Detail |
| --- | --- | --- |
| Backend | Flask or FastAPI on Render | Free web service, 512 MB RAM, no credit card, spins down after 15 minutes of inactivity (30 to 60 second wake-up), 750 free instance hours per month |
| Database | Neon (Postgres) | Free and permanent, 0.5 GB storage, 100 compute hours per month, automatic scale-to-zero with near-instant wake-up |
| Database alternative | Supabase | Free Postgres (500 MB) with built-in authentication, but pauses after a week of inactivity and needs a manual wake-up |
| Automatic ingestion | Python script via GitHub Actions | Free, unlimited cron on a public repo, fetches results (nba\_api or balldontlie) and odds (theoddsapi.com), writes directly to Neon |
| Frontend | PWA served by the same backend | Jinja2 plus manifest.json plus service worker, a single deployment to manage |
| Anti cold-start (optional) | cron-job.org or a GitHub Actions step | Regular ping to limit Render spin-downs on game nights |

Options ruled out: PythonAnywhere (free accounts restrict outbound connections to a whitelist, incompatible with nba\_api and theoddsapi.com by default), Railway and Fly.io (free tiers removed or now require a credit card), Render's free Postgres database (expires after 30 days and is permanently deleted).

Odds: theoddsapi.com's free tier gives 500 credits per month; one daily call with one market and one region uses roughly 30 credits per month, well under quota.

## Scoring system

Two scoring engines are implemented, selectable per league or per season through a config setting, so different groups can run different rules.

### Classic engine

Point values live in a config table in the database, not hardcoded, so they can be changed anytime without touching the code: point value for a correct game winner, point value for a correct series winner, and a bonus for the exact series score.

- 1 point for correctly predicting a game's winner
- 1 point for correctly predicting a series winner
- Bonus points for correctly predicting the exact series score (for example 4 to 2)

### Odds-based engine

Same structure, but points are multiplied by the odds:

- Game winner: 1 point multiplied by that game's odds, pulled automatically from theoddsapi.com
- Series winner: 1 point multiplied by the series-winner odds
- Series score: 1 point multiplied by the series-score odds

theoddsapi.com's free tier only covers game-level markets (moneyline, spreads, totals) and has no series-winner or series-score market. Since there are never more than about 15 playoff series at once, series-winner and series-score odds are entered manually by the admin (Benoit) into the config table, sourced from a sportsbook or odds comparison site, while game-level odds stay fully automated via the API.

## Next steps

- [ ] Data model (players, predictions, games, series, scores tables)
- [ ] Simple authentication for players: access link or code per player, no password (confirmed)
- [ ] Implementation of both scoring engines against the data model

## Data model

Classic relational structure on Postgres (Neon), five core tables.

| Table | Key fields | Notes |
| --- | --- | --- |
| players | id, name, access\_code | access\_code is the player's login link or code, no password |
| series | id, round, team\_a, team\_b, winner\_odds, score\_odds | winner\_odds and score\_odds are entered manually per series |
| games | id, series\_id, team\_a, team\_b, game\_date, result, game\_odds | game\_odds pulled automatically from theoddsapi.com; result filled in after ingestion |
| predictions | id, player\_id, game\_id (nullable), series\_id (nullable), predicted\_value, is\_correct, points\_earned | one row per player prediction, either tied to a game or to a series, never both |
| scoring\_config | id, engine, rule\_key, rule\_value | holds point values for the classic engine, keyed by engine and rule so they can change without code changes |

predictions.game\_id and predictions.series\_id are mutually exclusive: a game-level prediction fills game\_id and leaves series\_id empty, a series-level prediction (winner or exact score) does the reverse.

## Pre-playoffs bracket predictions

A separate bonus system, locked before the first playoff game, with one prediction per player per category:

- NBA champion
- Finals MVP
- Eastern Conference champion
- Western Conference champion

Each category carries its own bonus point value, held in scoring\_config alongside the classic and odds-based rules, so the payout per category can be tuned independently. Predictions lock at the start of the playoffs and cannot be changed once games begin.

Data model addition: a bracket\_predictions table (id, player\_id, category, predicted\_value, is\_correct, points\_earned), separate from the game and series predictions table since it is scored once at the end of the playoffs rather than after each game.
