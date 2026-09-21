-- Ajoute l'année de saison (convention balldontlie : année de DÉBUT de
-- saison, ex. 2025 pour la saison 2025-26 dont les playoffs se jouent en
-- avril-juin 2026) sur chaque série. Nécessaire pour que l'ingestion sache
-- distinguer deux séries entre les deux mêmes équipes, si elles se
-- recroisent une autre année. À exécuter une fois dans le SQL Editor de Neon
-- si ta base a été créée avant cet ajout (schema.sql à jour l'inclut déjà).
ALTER TABLE series ADD COLUMN IF NOT EXISTS season INTEGER;

-- Renseigne la saison des séries de test déjà créées (adapte si besoin) :
-- UPDATE series SET season = 2024 WHERE team_a = 'Oklahoma City Thunder' AND team_b = 'Indiana Pacers';
-- UPDATE series SET season = 2025 WHERE team_a = 'New York Knicks' AND team_b = 'San Antonio Spurs';
