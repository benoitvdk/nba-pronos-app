-- Needed for the NBA Cup: `group_name` remembers which of the 6 group-stage
-- groups a Series belongs to (only ever set for round = 'cup_group', see
-- app/models.py Series.group_name). Run once in Neon's SQL Editor if your
-- database was created before this addition (the current schema.sql
-- already includes this column for a fresh database).
ALTER TABLE series ADD COLUMN IF NOT EXISTS group_name VARCHAR(64);
