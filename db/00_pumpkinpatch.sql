CREATE DATABASE IF NOT EXISTS moonshotlabs;

USE moonshotlabs;

CREATE TABLE IF NOT EXISTS Team
(
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(50) UNIQUE,
    wins INT UNSIGNED DEFAULT 0,
    losses INT UNSIGNED DEFAULT 0,
    location VARCHAR(30) NOT NULL,
    coach_1 VARCHAR(50),
    coach_2 VARCHAR(50)
);

INSERT INTO Team (team_name, wins, losses, location, coach_1, coach_2)
    VALUES ('Red Sox', 5, 2, 'Boston, MA', 'Josh Holmes', 'Jack Poe'),
            ('Rays', 1, 6, 'Tampa, FL', 'Bob Holt', 'Vince Carter');


CREATE TABLE IF NOT EXISTS Team_Stats
(
    team_id INT,
    team_stat_id INT UNIQUE,
    avg_on_base DECIMAL(3,3) UNSIGNED,
    avg_era DECIMAL(4,2) UNSIGNED,
    total_hits INT UNSIGNED,
    total_rbi INT UNSIGNED,
    total_ks INT UNSIGNED,
    team_bat_avg DECIMAL(3,3) UNSIGNED,
    PRIMARY KEY(team_id, team_stat_id),
    CONSTRAINT fk_1
        FOREIGN KEY(team_id) REFERENCES Team(team_id)
            ON UPDATE CASCADE ON DELETE RESTRICT
);

INSERT INTO Team_Stats (team_id, team_stat_id, avg_on_base, avg_era, total_hits, total_rbi, total_ks, team_bat_avg)
    VALUES (1, 1, .333, 4.20, 5, 2, 13, .312);


CREATE TABLE IF NOT EXISTS Advanced_Stats
(
    team_id INT,
    adv_stat_id INT UNIQUE,
    wgdp DECIMAL(2,1),
    spd INT UNSIGNED,
    iso DECIMAL(2,2) UNSIGNED,
    bb_percent DECIMAL(3,3) UNSIGNED,
    k_percent DECIMAL(3,3) UNSIGNED,
    slugg_percent DECIMAL(3,3) UNSIGNED,
    run_diff DECIMAL(3,2),
    PRIMARY KEY(team_id, adv_stat_id),
    CONSTRAINT fk_2
        FOREIGN KEY(team_id) REFERENCES Team(team_id)
            ON UPDATE CASCADE ON DELETE RESTRICT
);

INSERT INTO Advanced_Stats (team_id, adv_stat_id, wgdp, spd, iso, bb_percent, k_percent, slugg_percent, run_diff)
    VALUES (1, 1, 2.1, 5, .65, .365, .222, .675, 3.4);


CREATE TABLE IF NOT EXISTS Bet_Stats
(
    team_id INT,
    bet_stat_id INT UNIQUE,
    home_money INT,
    ats DECIMAL(2,1),
    mov DECIMAL(3,2) UNSIGNED,
    cover_percent DECIMAL(3,3) UNSIGNED,
    PRIMARY KEY(team_id, bet_stat_id),
    CONSTRAINT fk_3
        FOREIGN KEY(team_id) REFERENCES Team(team_id)
            ON UPDATE CASCADE ON DELETE RESTRICT
);

INSERT INTO Bet_Stats (team_id, bet_stat_id, home_money, ats, mov, cover_percent)
    VALUES (1, 1, 5, 4.9, 1.67, .800);

CREATE TABLE IF NOT EXISTS Game
(
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    result CHAR(1),
    game_venue VARCHAR(50) NOT NULL,
    game_date DATE NOT NULL,
    game_time TIME NOT NULL,
    home_team VARCHAR(50) NOT NULL,
    away_team VARCHAR(50) NOT NULL,
    team_id INT,
    CONSTRAINT fk_4
        FOREIGN KEY(team_id) REFERENCES Team(team_id)
            ON UPDATE CASCADE ON DELETE RESTRICT
);

INSERT INTO Game (result, game_venue, game_date, game_time, home_team, away_team, team_id)
    VALUES ('W', 'Fenway', '2020-04-03', '13:30', 'Red Sox', 'Rays', 1);

CREATE TABLE IF NOT EXISTS Highlight
(
    clip_id INT AUTO_INCREMENT PRIMARY KEY,
    clip_format VARCHAR(10) NOT NULL,
    clip_length TIME,
    game_id INT,
    CONSTRAINT fk_5
        FOREIGN KEY(game_id) REFERENCES Game(game_id)
            ON UPDATE CASCADE ON DELETE CASCADE
);

INSERT INTO Highlight (clip_format, clip_length, game_id)
    VALUES ('.mov', '1:12', 1);

CREATE TABLE IF NOT EXISTS News_Article
(
    hyperlink VARCHAR(250) PRIMARY KEY,
    title VARCHAR(75),
    article_body MEDIUMTEXT
);

INSERT INTO News_Article (hyperlink, title, article_body)
    VALUES ('https://www.espn.com/redsox', 'Red Sox Article', 'We are two weeks into the 2023 MLB season, and most teams have played a dozen games of their 162-game schedule. In other words, it''s early. Perhaps too early to glean a whole lot from what has happened so far. But what''s the fun in that?');

CREATE TABLE IF NOT EXISTS Player
(
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    draft_year INT UNSIGNED,
    pick_number INT UNSIGNED,
    position VARCHAR(20),
    p_fName VARCHAR(50) NOT NULL,
    p_lName VARCHAR(50) NOT NULL,
    age INT UNSIGNED,
    college VARCHAR(50),
    salary INT UNSIGNED,
    jersey_number INT UNSIGNED,
    cur_team VARCHAR(50),
    team_id INT,
    CONSTRAINT fk_6
        FOREIGN KEY(team_id) REFERENCES Team(team_id)
            ON UPDATE CASCADE ON DELETE RESTRICT
);

INSERT INTO Player (draft_year, pick_number, position, p_fName, p_lName, age, college, salary, jersey_number, cur_team, team_id)
    VALUES (2015, 13, 'Catcher', 'Joel', 'Miller', 28, 'Northeastern', 500000, 10, 'Red Sox', 1);

CREATE TABLE IF NOT EXISTS Player_Stats
(
    player_id INT,
    player_stat_id INT UNIQUE,
    rbi INT UNSIGNED,
    hits INT UNSIGNED,
    ks INT UNSIGNED,
    whip DECIMAL(3,2),
    slg DECIMAL(3,3),
    obs DECIMAL(3,3),
    era DECIMAL(4,2),
    bat_avg DECIMAL(3,3),
    games_played INT UNSIGNED,
    PRIMARY KEY(player_id, player_stat_id),
    CONSTRAINT fk_7
        FOREIGN KEY(player_id) REFERENCES Player(player_id)
            ON UPDATE CASCADE ON DELETE RESTRICT
);

INSERT INTO Player_Stats (player_id, player_stat_id, rbi, hits, ks, whip, slg, obs, era, bat_avg, games_played)
    VALUES (1, 1, 30, 100, 0, 0.00, .456, .600, 00.00, .333, 50);

CREATE TABLE IF NOT EXISTS Game_Stats
(
    game_id INT,
    game_stat_id INT UNIQUE,
    home_ks INT UNSIGNED,
    away_ks INT UNSIGNED,
    home_score INT UNSIGNED,
    away_score INT UNSIGNED,
    game_bat_avg DECIMAL(3,3) UNSIGNED,
    home_homers INT UNSIGNED,
    away_homers INT UNSIGNED,
    PRIMARY KEY(game_id, game_stat_id),
    CONSTRAINT fk_8
        FOREIGN KEY(game_id) REFERENCES Game(game_id)
            ON UPDATE CASCADE ON DELETE RESTRICT
);

INSERT INTO Game_Stats (game_id, game_stat_id, home_ks, away_ks, home_score, away_score, game_bat_avg, home_homers, away_homers)
    VALUES (1, 1, 4, 6, 1, 0, .200, 0, 0);

CREATE TABLE IF NOT EXISTS Account_Profile
(
  SSN CHAR(9) PRIMARY KEY,
  sub_type VARCHAR(15) NOT NULL,
  sub_length_months INT UNSIGNED NOT NULL,
  age INT UNSIGNED,
  fName VARCHAR(50) NOT NULL,
  lName VARCHAR(50) NOT NULL,
  screen_time_hours INT UNSIGNED,
  username VARCHAR(50) UNIQUE
);

INSERT INTO Account_Profile (SSN, sub_type, sub_length_months, age, fName, lName, screen_time_hours, username)
    VALUES ('098026789', 'Basic', 5, 70, 'Marco', 'Milton', 20, 'mmilton5');


CREATE TABLE IF NOT EXISTS Bet_Slip
(
    bet_id INT AUTO_INCREMENT PRIMARY KEY,
    bet_type VARCHAR(20) NOT NULL,
    bet_description VARCHAR(200),
    payout DECIMAL(10,2),
    amount DECIMAL(8,2) NOT NULL,
    return_rate DECIMAL(4,3),
    game_id INT,
    SSN CHAR(9),
    CONSTRAINT fk_9
        FOREIGN KEY(game_id) REFERENCES Game(game_id)
            ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_10
        FOREIGN KEY(SSN) REFERENCES Account_Profile(SSN)
            ON UPDATE RESTRICT ON DELETE RESTRICT
);

INSERT INTO Bet_Slip (bet_type, bet_description, payout, amount, return_rate, game_id, SSN)
    VALUES ('Over/Under', 'Placed an Over/Under Bet on Boston vs the Rays', 20.00, 10.00, 2.000, 1, '098026789');

CREATE TABLE IF NOT EXISTS Earnings_Account
(
    SSN CHAR(9),
    account_no INT UNIQUE,
    balance DECIMAL(14,2),
    PRIMARY KEY(SSN, account_no),
    CONSTRAINT fk_11
        FOREIGN KEY(SSN) REFERENCES Account_Profile(SSN)
            ON UPDATE RESTRICT ON DELETE RESTRICT
);

INSERT INTO Earnings_Account (SSN, account_no, balance)
    VALUES ('098026789', 1, 50.00);

CREATE TABLE IF NOT EXISTS Injury_Update
(
    player_id INT,
    injury_id INT,
    title VARCHAR(75),
    upd_body MEDIUMTEXT,
    injury_date DATE,
    PRIMARY KEY(player_id, injury_id),
    CONSTRAINT fk_12
        FOREIGN KEY(player_id) REFERENCES Player(player_id)
            ON UPDATE CASCADE ON DELETE CASCADE
);

INSERT INTO Injury_Update (player_id, injury_id, title, upd_body, injury_date)
    VALUES (1, 1, 'Joel Miller Injury!', 'Joel Miller has injured his hand for the rest of the season.', '2020-04-03');

CREATE TABLE IF NOT EXISTS NewsArticle_Game
(
    game_id INT,
    hyperlink VARCHAR(250),
    PRIMARY KEY(game_id, hyperlink),
    CONSTRAINT fk_13
        FOREIGN KEY(game_id) REFERENCES Game(game_id)
            ON UPDATE CASCADE ON DELETE RESTRICT,
     CONSTRAINT fk_14
        FOREIGN KEY(hyperlink) REFERENCES News_Article(hyperlink)
            ON UPDATE CASCADE ON DELETE CASCADE
);

INSERT INTO NewsArticle_Game (game_id, hyperlink)
    VALUES (1, 'https://www.espn.com/redsox');

CREATE TABLE IF NOT EXISTS Highlight_Keywords
(
    clip_id INT,
    keywords VARCHAR(30),
    PRIMARY KEY(clip_id, keywords),
    CONSTRAINT fk_15
        FOREIGN KEY(clip_id) REFERENCES Highlight(clip_id)
            ON UPDATE CASCADE ON DELETE CASCADE
);

INSERT INTO Highlight_Keywords (clip_id, keywords)
    VALUES (1, 'Dinger');
