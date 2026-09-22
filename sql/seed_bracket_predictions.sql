-- Seed script: realistic pre-playoffs "bracket" predictions for the two
-- test players (ids 3 and 4 - check these still match your test players
-- before running this, e.g.: SELECT id, name FROM players WHERE id IN (3, 4);).
--
-- East/West conference champion picks match the fictional bracket already
-- seeded (see sql/seed_test_playoffs.sql): New York Knicks won the East,
-- San Antonio Spurs won the West. Player 3 gets both right; player 4 gets
-- a plausible near-miss on the East (Cleveland Cavaliers, who actually
-- lost the East finals to the Knicks in that seeded bracket).
--
-- NBA champion / Finals MVP depend on the ACTUAL result of your existing
-- New York Knicks vs San Antonio Spurs finals series (not part of the
-- fictional bracket, so its real winner isn't known here) - the two
-- players are split one per team so exactly one of them ends up right
-- whatever that result turns out to be.

INSERT INTO bracket_predictions (player_id, category, predicted_value) VALUES
  (3, 'east_champion', 'New York Knicks'),
  (3, 'west_champion', 'San Antonio Spurs'),
  (3, 'nba_champion', 'New York Knicks'),
  (3, 'finals_mvp', 'Jalen Brunson'),
  (4, 'east_champion', 'Cleveland Cavaliers'),
  (4, 'west_champion', 'San Antonio Spurs'),
  (4, 'nba_champion', 'San Antonio Spurs'),
  (4, 'finals_mvp', 'Victor Wembanyama')
ON CONFLICT (player_id, category) DO UPDATE SET
  predicted_value = EXCLUDED.predicted_value,
  is_correct = NULL,
  points_earned = NULL;

-- East/West are already decided by the seeded bracket, so you can score
-- them right away:
--   python -m scripts.score_bracket --category east_champion --winner "New York Knicks"
--   python -m scripts.score_bracket --category west_champion --winner "San Antonio Spurs"
--
-- NBA champion / Finals MVP: score once you know the real winner already
-- recorded for your Knicks-Spurs finals series, e.g.:
--   python -m scripts.score_bracket --category nba_champion --winner "New York Knicks"
--   python -m scripts.score_bracket --category finals_mvp --winner "Jalen Brunson"
