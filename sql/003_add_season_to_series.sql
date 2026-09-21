-- Adds the season year (balldontlie convention: STARTING year of the
-- season, e.g. 2025 for the 2025-26 season whose playoffs are played in
-- April-June 2026) on each series. Needed so ingestion can tell apart two
-- series between the same two teams, if they meet again in another year.
-- Run once in Neon's SQL Editor if your database was created before this
-- addition (the current schema.sql already includes it).
ALTER TABLE series ADD COLUMN IF NOT EXISTS season INTEGER;

-- Fill in the season for already-created test series (adapt as needed):
-- UPDATE series SET season = 2024 WHERE team_a = 'Oklahoma City Thunder' AND team_b = 'Indiana Pacers';
-- UPDATE series SET season = 2025 WHERE team_a = 'New York Knicks' AND team_b = 'San Antonio Spurs';
