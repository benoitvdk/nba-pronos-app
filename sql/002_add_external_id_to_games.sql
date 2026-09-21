-- Ajout nécessaire pour le script d'ingestion (scripts/ingest.py), qui doit
-- pouvoir relancer l'import sans créer de matchs en double. À exécuter une
-- fois dans le SQL Editor de Neon si ta base a été créée avant cet ajout
-- (schema.sql à jour inclut déjà cette colonne pour une base neuve).
ALTER TABLE games ADD COLUMN IF NOT EXISTS external_id VARCHAR(32) UNIQUE;
