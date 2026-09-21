-- Needed for the ingestion script (scripts/ingest.py), which must be able
-- to re-run the import without creating duplicate games. Run once in
-- Neon's SQL Editor if your database was created before this addition
-- (the current schema.sql already includes this column for a fresh
-- database).
ALTER TABLE games ADD COLUMN IF NOT EXISTS external_id VARCHAR(32) UNIQUE;
