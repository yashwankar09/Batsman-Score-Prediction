create database IPL_2024;
use IPL_2024;

CREATE TABLE batsman (
    id VARCHAR(20),
    match_date VARCHAR(15),
    season INT(5),
    batsman VARCHAR(255),
    runs_scored INT(10),
    balls_played INT(10),
    minutes_while_batting INT(10),
    4s INT(10),
    6s INT(10),
    strike_rate FLOAT4(10),
    wicket_by VARCHAR(255),
    is_notout INT(2),
    is_out INT(2),
    is_runout INT(2),
    batting_team VARCHAR(255),
    bowling_team VARCHAR(255),
    venue VARCHAR(255),
    day_or_night VARCHAR(255),
    captain VARCHAR(255),
    toss_winner VARCHAR(255),
    toss_decision VARCHAR(255),
    winner VARCHAR(255),
    win_by VARCHAR(255),
    summary VARCHAR(255)
);

CREATE TABLE bowler (
    id VARCHAR(20),
    match_date VARCHAR(15),
    season INT(5),
    bowler VARCHAR(255),
    wicket INT(5),
    overs float4(5),
    maidan INT(5),
    runs INT(5),
    Econ FLOAT4(10),
    0s_conceded INT(5),
    4s_conceded INT(5),
    6s_conceded INT(5),
    wide_balls INT(5),
    no_balls INT(5),
    batting_team VARCHAR(255),
    bowling_team VARCHAR(255),
    venue VARCHAR(255),
    day_or_night VARCHAR(255),
    toss_winner VARCHAR(255),
    toss_decision VARCHAR(255),
    winner VARCHAR(255),
    win_by VARCHAR(255),
    summary VARCHAR(255)
);

CREATE TABLE POTM (
    id VARCHAR(20),
    player_name VARCHAR(255),
    team_name VARCHAR(255)
);

CREATE TABLE Extra_runs (
    id VARCHAR(20),
    runs INT(10),
    batting_team VARCHAR(255)
);