INSERT INTO scoring_config (engine, rule_key, rule_value) VALUES
  ('classic', 'game_winner_points', 1),
  ('classic', 'series_winner_points', 1),
  ('classic', 'series_score_bonus_points', 3),
  ('odds_based', 'game_winner_points', 1),
  ('odds_based', 'series_winner_points', 1),
  ('odds_based', 'series_score_points', 1),
  ('bracket', 'nba_champion_points', 10),
  ('bracket', 'finals_mvp_points', 5),
  ('bracket', 'east_champion_points', 5),
  ('bracket', 'west_champion_points', 5)
ON CONFLICT (engine, rule_key) DO NOTHING;
