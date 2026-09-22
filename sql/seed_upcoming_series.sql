-- Test-only fictional series with upcoming, unplayed games (no result yet,
-- game_date in the future), to check the "a venir" / open-for-prediction
-- UI: series winner/score forms and the game-by-game team buttons, before
-- anything locks. Dates are relative to now(), so they stay "in the days
-- ahead" whenever you actually run this script.
--
-- No predictions are inserted on purpose - log in as one of the test
-- players and submit picks through the UI itself to test that flow.

INSERT INTO series (season, round, team_a, team_b)
VALUES (2026, 'first_round', 'Phoenix Suns', 'Dallas Mavericks');

INSERT INTO games (series_id, team_a, team_b, game_date)
SELECT s.id, 'Phoenix Suns', 'Dallas Mavericks', now() + interval '2 days'
FROM series s
WHERE s.season = 2026 AND s.round = 'first_round' AND s.team_a = 'Phoenix Suns' AND s.team_b = 'Dallas Mavericks';

INSERT INTO games (series_id, team_a, team_b, game_date)
SELECT s.id, 'Phoenix Suns', 'Dallas Mavericks', now() + interval '4 days'
FROM series s
WHERE s.season = 2026 AND s.round = 'first_round' AND s.team_a = 'Phoenix Suns' AND s.team_b = 'Dallas Mavericks';

INSERT INTO games (series_id, team_a, team_b, game_date)
SELECT s.id, 'Phoenix Suns', 'Dallas Mavericks', now() + interval '6 days'
FROM series s
WHERE s.season = 2026 AND s.round = 'first_round' AND s.team_a = 'Phoenix Suns' AND s.team_b = 'Dallas Mavericks';
