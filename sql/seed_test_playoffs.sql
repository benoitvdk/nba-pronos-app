-- Seed script: full 2025-26 playoffs bracket (test/fictional matchups and
-- results, only meant to populate the app with realistic-looking data for
-- testing - these are NOT the real 2025-26 NBA playoff results) plus a
-- realistic mix of correct/incorrect predictions for the two test players
-- (ids 3 and 4 below - check these still match your test players before
-- running this, e.g. with: SELECT id, name FROM players WHERE id IN (3, 4);).
--
-- The existing New York Knicks vs San Antonio Spurs finals series is left
-- untouched; this script adds the 14 series leading up to it (8 first
-- round, 4 conference semifinals, 2 conference finals).
--
-- Series/games are looked up by (season, round, team_a, team_b) and exact
-- game_date rather than by id, so this can be re-run/inspected safely -
-- but running it twice would create duplicate series (no unique
-- constraint on that combination), so only run it once.
--
-- After running this, recompute is_correct/points_earned with:
--   python -m scripts.run_scoring --engine classic

BEGIN;

-- 1. first_round: Boston Celtics vs Miami Heat (winner: Boston Celtics, 4-1)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'first_round', 'Boston Celtics', 'Miami Heat');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Boston Celtics', 'Miami Heat', '2026-04-19 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Boston Celtics', 'Miami Heat', '2026-04-21 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Boston Celtics', 'Miami Heat', '2026-04-23 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Boston Celtics', 'Miami Heat', '2026-04-25 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Boston Celtics', 'Miami Heat', '2026-04-27 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_a:4-1' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_a:4-0' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-19 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-19 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-21 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-21 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-23 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-23 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-25 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-25 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-27 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-27 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Miami Heat';


-- 2. first_round: Cleveland Cavaliers vs Chicago Bulls (winner: Cleveland Cavaliers, 4-2)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'first_round', 'Cleveland Cavaliers', 'Chicago Bulls');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Cleveland Cavaliers', 'Chicago Bulls', '2026-04-19 23:30:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Cleveland Cavaliers', 'Chicago Bulls', '2026-04-21 23:30:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Cleveland Cavaliers', 'Chicago Bulls', '2026-04-23 23:30:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Cleveland Cavaliers', 'Chicago Bulls', '2026-04-25 23:30:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Cleveland Cavaliers', 'Chicago Bulls', '2026-04-27 23:30:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Cleveland Cavaliers', 'Chicago Bulls', '2026-04-29 23:30:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_a:4-2' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_b' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_b:4-2' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-19 23:30:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-19 23:30:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-21 23:30:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-21 23:30:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-23 23:30:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-23 23:30:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-25 23:30:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-25 23:30:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-27 23:30:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-27 23:30:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-29 23:30:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-29 23:30:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Cleveland Cavaliers' AND s.team_b = 'Chicago Bulls';


-- 3. first_round: New York Knicks vs Orlando Magic (winner: New York Knicks, 4-3)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'first_round', 'New York Knicks', 'Orlando Magic');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Orlando Magic', '2026-04-20 00:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Orlando Magic', '2026-04-22 00:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Orlando Magic', '2026-04-24 00:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Orlando Magic', '2026-04-26 00:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Orlando Magic', '2026-04-28 00:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Orlando Magic', '2026-04-30 00:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Orlando Magic', '2026-05-02 00:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_a:4-3' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_a:4-3' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-20 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-20 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-22 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-22 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-24 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-24 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-26 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-26 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-28 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-28 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-30 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-30 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-02 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-02 00:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'New York Knicks' AND s.team_b = 'Orlando Magic';


-- 4. first_round: Milwaukee Bucks vs Indiana Pacers (winner: Indiana Pacers, 4-3)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'first_round', 'Milwaukee Bucks', 'Indiana Pacers');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Milwaukee Bucks', 'Indiana Pacers', '2026-04-20 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Milwaukee Bucks', 'Indiana Pacers', '2026-04-22 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Milwaukee Bucks', 'Indiana Pacers', '2026-04-24 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Milwaukee Bucks', 'Indiana Pacers', '2026-04-26 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Milwaukee Bucks', 'Indiana Pacers', '2026-04-28 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Milwaukee Bucks', 'Indiana Pacers', '2026-04-30 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Milwaukee Bucks', 'Indiana Pacers', '2026-05-02 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_a:4-0' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_b' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_b:4-3' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-20 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-20 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-22 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-22 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-24 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-24 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-26 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-26 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-28 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-28 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-30 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-30 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-02 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-02 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Milwaukee Bucks' AND s.team_b = 'Indiana Pacers';


-- 5. first_round: Oklahoma City Thunder vs Golden State Warriors (winner: Oklahoma City Thunder, 4-1)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'first_round', 'Oklahoma City Thunder', 'Golden State Warriors');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Oklahoma City Thunder', 'Golden State Warriors', '2026-04-19 02:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Oklahoma City Thunder', 'Golden State Warriors', '2026-04-21 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Oklahoma City Thunder', 'Golden State Warriors', '2026-04-23 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Oklahoma City Thunder', 'Golden State Warriors', '2026-04-25 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Oklahoma City Thunder', 'Golden State Warriors', '2026-04-27 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_a:4-1' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_b' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_b:4-0' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-19 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-19 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-21 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-21 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-23 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-23 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-25 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-25 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-27 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-27 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Golden State Warriors';


-- 6. first_round: Denver Nuggets vs LA Clippers (winner: Denver Nuggets, 4-3)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'first_round', 'Denver Nuggets', 'LA Clippers');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Denver Nuggets', 'LA Clippers', '2026-04-20 02:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Denver Nuggets', 'LA Clippers', '2026-04-22 02:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Denver Nuggets', 'LA Clippers', '2026-04-24 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Denver Nuggets', 'LA Clippers', '2026-04-26 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Denver Nuggets', 'LA Clippers', '2026-04-28 02:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Denver Nuggets', 'LA Clippers', '2026-04-30 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Denver Nuggets', 'LA Clippers', '2026-05-02 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_a:4-3' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_a:4-2' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-20 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-20 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-22 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-22 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-24 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-24 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-26 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-26 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-28 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-28 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-30 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-30 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-02 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-02 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Denver Nuggets' AND s.team_b = 'LA Clippers';


-- 7. first_round: San Antonio Spurs vs Los Angeles Lakers (winner: San Antonio Spurs, 4-2)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'first_round', 'San Antonio Spurs', 'Los Angeles Lakers');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Los Angeles Lakers', '2026-04-19 03:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Los Angeles Lakers', '2026-04-21 03:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Los Angeles Lakers', '2026-04-23 03:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Los Angeles Lakers', '2026-04-25 03:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Los Angeles Lakers', '2026-04-27 03:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Los Angeles Lakers', '2026-04-29 03:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_a:4-2' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_b' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_b:4-0' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-19 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-19 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-21 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-21 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-23 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-23 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-25 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-25 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-27 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-27 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-29 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-29 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Los Angeles Lakers';


-- 8. first_round: Houston Rockets vs Minnesota Timberwolves (winner: Minnesota Timberwolves, 4-3)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'first_round', 'Houston Rockets', 'Minnesota Timberwolves');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Houston Rockets', 'Minnesota Timberwolves', '2026-04-20 03:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Houston Rockets', 'Minnesota Timberwolves', '2026-04-22 03:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Houston Rockets', 'Minnesota Timberwolves', '2026-04-24 03:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Houston Rockets', 'Minnesota Timberwolves', '2026-04-26 03:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Houston Rockets', 'Minnesota Timberwolves', '2026-04-28 03:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Houston Rockets', 'Minnesota Timberwolves', '2026-04-30 03:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Houston Rockets', 'Minnesota Timberwolves', '2026-05-02 03:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_b' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_b:4-0' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_b' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_b:4-3' FROM series s WHERE s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-20 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-20 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-22 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-22 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-24 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-24 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-26 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-26 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-28 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-28 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-30 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-04-30 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-02 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-02 03:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'first_round' AND s.team_a = 'Houston Rockets' AND s.team_b = 'Minnesota Timberwolves';


-- 9. conf_semis: Boston Celtics vs Cleveland Cavaliers (winner: Cleveland Cavaliers, 4-3)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'conf_semis', 'Boston Celtics', 'Cleveland Cavaliers');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Boston Celtics', 'Cleveland Cavaliers', '2026-05-05 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Boston Celtics', 'Cleveland Cavaliers', '2026-05-07 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Boston Celtics', 'Cleveland Cavaliers', '2026-05-09 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Boston Celtics', 'Cleveland Cavaliers', '2026-05-11 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Boston Celtics', 'Cleveland Cavaliers', '2026-05-13 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Boston Celtics', 'Cleveland Cavaliers', '2026-05-15 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Boston Celtics', 'Cleveland Cavaliers', '2026-05-17 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_b' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_b:4-3' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_b' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_b:4-3' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-05 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-05 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-07 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-07 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-09 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-09 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-11 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-11 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-13 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-13 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-15 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-15 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-17 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-17 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Boston Celtics' AND s.team_b = 'Cleveland Cavaliers';


-- 10. conf_semis: New York Knicks vs Indiana Pacers (winner: New York Knicks, 4-2)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'conf_semis', 'New York Knicks', 'Indiana Pacers');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Indiana Pacers', '2026-05-06 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Indiana Pacers', '2026-05-08 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Indiana Pacers', '2026-05-10 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Indiana Pacers', '2026-05-12 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Indiana Pacers', '2026-05-14 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Indiana Pacers', '2026-05-16 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_b' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_b:4-1' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_a:4-1' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-06 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-06 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-08 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-08 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-10 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-10 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-12 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-12 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-14 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-14 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-16 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-16 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'New York Knicks' AND s.team_b = 'Indiana Pacers';


-- 11. conf_semis: Oklahoma City Thunder vs Minnesota Timberwolves (winner: Oklahoma City Thunder, 4-2)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'conf_semis', 'Oklahoma City Thunder', 'Minnesota Timberwolves');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Oklahoma City Thunder', 'Minnesota Timberwolves', '2026-05-05 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Oklahoma City Thunder', 'Minnesota Timberwolves', '2026-05-07 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Oklahoma City Thunder', 'Minnesota Timberwolves', '2026-05-09 02:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Oklahoma City Thunder', 'Minnesota Timberwolves', '2026-05-11 02:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Oklahoma City Thunder', 'Minnesota Timberwolves', '2026-05-13 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'Oklahoma City Thunder', 'Minnesota Timberwolves', '2026-05-15 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_b' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_b:4-0' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_b' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_b:4-0' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-05 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-05 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-07 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-07 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-09 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-09 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-11 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-11 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-13 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-13 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-15 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-15 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'Oklahoma City Thunder' AND s.team_b = 'Minnesota Timberwolves';


-- 12. conf_semis: San Antonio Spurs vs Denver Nuggets (winner: San Antonio Spurs, 4-3)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'conf_semis', 'San Antonio Spurs', 'Denver Nuggets');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Denver Nuggets', '2026-05-06 02:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Denver Nuggets', '2026-05-08 02:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Denver Nuggets', '2026-05-10 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Denver Nuggets', '2026-05-12 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Denver Nuggets', '2026-05-14 02:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Denver Nuggets', '2026-05-16 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Denver Nuggets', '2026-05-18 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_a:4-2' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_b' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_b:4-1' FROM series s WHERE s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-06 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-06 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-08 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-08 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-10 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-10 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-12 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-12 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-14 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-14 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-16 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-16 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-18 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-18 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_semis' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Denver Nuggets';


-- 13. conf_finals: New York Knicks vs Cleveland Cavaliers (winner: New York Knicks, 4-3)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'conf_finals', 'New York Knicks', 'Cleveland Cavaliers');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Cleveland Cavaliers', '2026-05-20 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Cleveland Cavaliers', '2026-05-22 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Cleveland Cavaliers', '2026-05-24 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Cleveland Cavaliers', '2026-05-26 23:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Cleveland Cavaliers', '2026-05-28 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Cleveland Cavaliers', '2026-05-30 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'New York Knicks', 'Cleveland Cavaliers', '2026-06-01 23:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_a:4-2' FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_b' FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_b:4-0' FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-20 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-20 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-22 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-22 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-24 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-24 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-26 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-26 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-28 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-28 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-30 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-30 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-06-01 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-06-01 23:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'New York Knicks' AND s.team_b = 'Cleveland Cavaliers';


-- 14. conf_finals: San Antonio Spurs vs Oklahoma City Thunder (winner: San Antonio Spurs, 4-2)
INSERT INTO series (season, round, team_a, team_b) VALUES (2025, 'conf_finals', 'San Antonio Spurs', 'Oklahoma City Thunder');

INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Oklahoma City Thunder', '2026-05-20 02:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Oklahoma City Thunder', '2026-05-22 02:00:00+00'::timestamptz, 'team_b'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Oklahoma City Thunder', '2026-05-24 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Oklahoma City Thunder', '2026-05-26 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Oklahoma City Thunder', '2026-05-28 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO games (series_id, team_a, team_b, game_date, result)
SELECT s.id, 'San Antonio Spurs', 'Oklahoma City Thunder', '2026-05-30 02:00:00+00'::timestamptz, 'team_a'
FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';

INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 3, s.id, 'series_score', 'team_a:4-0' FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_winner', 'team_a' FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, series_id, prediction_type, predicted_value)
SELECT 4, s.id, 'series_score', 'team_a:4-2' FROM series s WHERE s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';

INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-20 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-20 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-22 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-22 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-24 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-24 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_b'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-26 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-26 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-28 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-28 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 3, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-30 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';
INSERT INTO predictions (player_id, game_id, prediction_type, predicted_value)
SELECT 4, g.id, 'game_winner', 'team_a'
FROM games g JOIN series s ON g.series_id = s.id WHERE g.game_date = '2026-05-30 02:00:00+00'::timestamptz AND s.season = 2025 AND s.round = 'conf_finals' AND s.team_a = 'San Antonio Spurs' AND s.team_b = 'Oklahoma City Thunder';


COMMIT;
