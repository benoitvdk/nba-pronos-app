-- Test-only NBA Cup group-stage data, to check the Cup UI (dashboard,
-- single-game "series" card, group tag, bracket page) before balldontlie
-- has actually loaded the 2026-27 schedule into their database.
--
-- Real matchups from the real 2026-27 groups (confirmed on NBA.com, "Emirates
-- NBA Cup 2026 groups announced"), with fictional near-future dates so the
-- "à venir" / open-for-prediction UI has something to show. No predictions
-- are inserted on purpose - log in as a test player and submit picks
-- through the UI itself.
--
-- IMPORTANT: these rows have no external_id (NULL), so once real ingestion
-- (scripts/ingest.py --season-type ist) picks up the real games, it will
-- NOT recognize them as the same game (it matches on external_id) and will
-- add a second Game row under the same Series instead of updating this one.
-- Delete these test games before running real ingestion for real - see the
-- DELETE at the bottom (commented out on purpose).

-- East Group C
INSERT INTO series (season, round, team_a, team_b, group_name)
VALUES (2026, 'cup_group', 'Boston Celtics', 'Atlanta Hawks', 'East Group C');

INSERT INTO games (series_id, team_a, team_b, game_date)
SELECT s.id, 'Boston Celtics', 'Atlanta Hawks', now() + interval '3 days'
FROM series s
WHERE s.season = 2026 AND s.round = 'cup_group' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Atlanta Hawks';

-- West Group A
INSERT INTO series (season, round, team_a, team_b, group_name)
VALUES (2026, 'cup_group', 'Denver Nuggets', 'Phoenix Suns', 'West Group A');

INSERT INTO games (series_id, team_a, team_b, game_date)
SELECT s.id, 'Denver Nuggets', 'Phoenix Suns', now() + interval '5 days'
FROM series s
WHERE s.season = 2026 AND s.round = 'cup_group' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'Phoenix Suns';

-- East Group B - already "played" (past date + a result), to check the
-- locked/finished state and the game-winner scoring path.
INSERT INTO series (season, round, team_a, team_b, group_name)
VALUES (2026, 'cup_group', 'New York Knicks', 'Miami Heat', 'East Group B');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Miami Heat', now() - interval '1 day', 'team_a'
FROM series s
WHERE s.season = 2026 AND s.round = 'cup_group' AND s.team_a = 'New York Knicks' AND s.team_b = 'Miami Heat';

-- Clean-up once real ingestion has taken over (uncomment and run):
-- DELETE FROM games WHERE external_id IS NULL AND series_id IN (
--   SELECT id FROM series WHERE round = 'cup_group' AND season = 2026
--   AND (team_a, team_b) IN (
--     ('Boston Celtics', 'Atlanta Hawks'),
--     ('Denver Nuggets', 'Phoenix Suns'),
--     ('New York Knicks', 'Miami Heat')
--   )
-- );
-- DELETE FROM series WHERE round = 'cup_group' AND season = 2026
--   AND (team_a, team_b) IN (
--     ('Boston Celtics', 'Atlanta Hawks'),
--     ('Denver Nuggets', 'Phoenix Suns'),
--     ('New York Knicks', 'Miami Heat')
--   );
