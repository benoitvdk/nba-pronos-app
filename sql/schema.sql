
CREATE TABLE players (
	id SERIAL NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	access_code VARCHAR(64) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (access_code)
);


CREATE TABLE scoring_config (
	id SERIAL NOT NULL, 
	engine VARCHAR(16) NOT NULL, 
	rule_key VARCHAR(64) NOT NULL, 
	rule_value FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_scoring_config_engine_rule UNIQUE (engine, rule_key)
);


CREATE TABLE series (
	id SERIAL NOT NULL,
	season INTEGER,
	round VARCHAR(32) NOT NULL,
	team_a VARCHAR(64) NOT NULL,
	team_b VARCHAR(64) NOT NULL,
	winner_odds JSON,
	score_odds JSON,
	group_name VARCHAR(64),
	PRIMARY KEY (id)
);


CREATE TABLE bracket_predictions (
	id SERIAL NOT NULL, 
	player_id INTEGER NOT NULL, 
	category VARCHAR(32) NOT NULL, 
	predicted_value VARCHAR(64) NOT NULL, 
	is_correct BOOLEAN, 
	points_earned FLOAT, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_bracket_prediction_player_category UNIQUE (player_id, category), 
	FOREIGN KEY(player_id) REFERENCES players (id)
);


CREATE TABLE games (
	id SERIAL NOT NULL, 
	series_id INTEGER NOT NULL, 
	team_a VARCHAR(64) NOT NULL, 
	team_b VARCHAR(64) NOT NULL, 
	game_date TIMESTAMP WITH TIME ZONE NOT NULL, 
	result VARCHAR(16), 
	game_odds JSON, 
	external_id VARCHAR(32), 
	PRIMARY KEY (id), 
	FOREIGN KEY(series_id) REFERENCES series (id), 
	UNIQUE (external_id)
);


CREATE TABLE predictions (
	id SERIAL NOT NULL, 
	player_id INTEGER NOT NULL, 
	game_id INTEGER, 
	series_id INTEGER, 
	prediction_type VARCHAR(16) NOT NULL, 
	predicted_value VARCHAR(32) NOT NULL, 
	is_correct BOOLEAN, 
	points_earned FLOAT, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_prediction_game_xor_series CHECK ((game_id IS NOT NULL AND series_id IS NULL) OR (game_id IS NULL AND series_id IS NOT NULL)), 
	CONSTRAINT uq_prediction_player_game UNIQUE (player_id, game_id), 
	CONSTRAINT uq_prediction_player_series_type UNIQUE (player_id, series_id, prediction_type), 
	FOREIGN KEY(player_id) REFERENCES players (id), 
	FOREIGN KEY(game_id) REFERENCES games (id), 
	FOREIGN KEY(series_id) REFERENCES series (id)
);

