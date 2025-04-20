use IPL_2024;

/* Batting data validation.;*/

select * from batsman;
select count(distinct id),count(*) from batsman;
-- 74	1132;

select * from batsman
where id = '45th';

select min(runs_scored) as min_runs,max(runs_scored) as max_runs,
min(balls_played) as min_balls_played,max(balls_played) as max_balls_played,
min(minutes_while_batting) as min_min,max(minutes_while_batting) as max_min,
min(4s) as min_4s,max(4s) as max_4s,
min(6s) as min_6s,max(6s) as max_6s,
min(strike_rate) as min_strike_rate,max(strike_rate) as max_strike_rate
from batsman;

select * from batsman 
where strike_rate = 600;

select * from batsman 
where runs_scored = 140;

-- validating runs scored by batsman;

select batsman,count(distinct id) as no_of_match,sum(runs_scored) as total_runs,sum(runs_scored)/(count(distinct id)-sum(is_notout)) as average,sum(is_notout)
,max(runs_scored) as highest_score,
sum(4s) as 4s,sum(6s) as 6s,round(sum(runs_scored)/sum(balls_played) * 100,2) as strike_rate,
sum(balls_played) as balls_faced,
sum(case when runs_scored >= 100 then 1 else 0 end) as century,
sum(case when runs_scored >= 50 and runs_scored < 100 then 1 else 0 end) as hf
from batsman
group by 1
order by sum(runs_scored) desc;

with temp1 as (
select distinct(id) as id,
case when id not in ('Qualifier1 (N)','Final','Qualifier2 (N)','Eliminator') then regexp_replace(id,'[^0-9]','')
when id = 'Qualifier1 (N)' then 71
when id = 'Qualifier2 (N)' then 73
when id = 'Eliminator' then 72
when id = 'Final' then 74
else id end as id_num
-- rank() over(order by id) as w1
from
batsman
order by cast(regexp_replace(id,'[^0-9]','') as signed) desc)
select a.*,cast(t1.id_num as signed) as id_num from batsman a
left join
temp1 as t1
on a.id = t1.id
order by cast(t1.id_num as signed)  desc;

select batsman,id,
dense_rank() over(partition by id order by batsman) as r1,
row_number() over(partition by id order by id) as r2
from batsman;

select distinct id,batsman,bowling_team,runs_scored,
sum(runs_scored) over(partition by batsman,bowling_team ) as runs_against_teams,
row_number() over(partition by batsman order by id) as no_of_innings,
count(id) over(partition by bowling_team,batsman) as no_of_matches_against_teams,
sum(runs_scored) over(partition by batsman) as total_runs
from batsman
order by batsman desc;

select batsman,bowling_team,sum(runs_scored) as rs
from batsman
group by 1,2
order by 1 desc;

-- validating bowling data

select * from bowler;

with BBI_data as(
select b.bowler, concat_ws('/',a.wk,min(b.runs)) as BBI
from bowler b
inner join
(select bowler,max(wicket) as wk
from bowler
group by 1
order by sum(wicket) desc) a
on a.bowler=b.bowler
and b.wicket=a.wk
group by 1)
SELECT 
    y.bowler,
    SUM(wicket) AS wicket,
    round(SUM(overs),1) AS overs,
    SUM(runs) AS runs,
    SUM(maidan) maidens,
    SUM(4s_conceded) AS 4s,
    SUM(6s_conceded) AS 6s,
    max(BBI) as BBI,
    sum(case when wicket >= 5 then 1 else 0 end) as 5w,
    sum(case when wicket = 4 then 1 else 0 end) as 4w,
    round(sum(runs)/sum(wicket),2) as average,
    round(sum(runs)/sum(overs),2) as Econ,
    round((sum(overs)*6)/sum(wicket),2) as S_R 
FROM
    bowler y
        LEFT JOIN
        BBI_Data z
	ON y.bowler = z.bowler
GROUP BY 1
ORDER BY SUM(wicket) DESC ;

select * from bowler;

select id,bowler,wicket,batting_team,
sum(wicket) over(partition by batting_team,bowler) as wicket_against_batting_team,
count(id) over(partition by batting_team,bowler) as matches_againest_teams,
row_number() over(partition by bowler order by id) as no_of_matches,
first_value(wicket) over(partition by bowler) as fw,
last_value(wicket) over(partition by bowler) as lw
from bowler
order by 2 desc;

-- Joining batsman & bowler tables
drop table t1;
with modified_batting as (
select id,batting_team,bowling_team,batsman,
case when wicket_by = 'Kumar' and bowling_team = 'Sunrisers Hyderabad' then 'Bhuvneshwar Kumar'
else wicket_by end as bolwer_updated
from batsman)
select a.id,a.batsman,a.batting_team,a.bowling_team,a.bolwer_updated,
coalesce(b.bowler,'-'),coalesce(b.batting_team,a.batting_team) as bt1, coalesce(b.bowling_team,a.bowling_team) as bt2,
count(b.wicket) over(partition by b.bowler,b.id) as no_of_wickets
from modified_batting a
left join bowler b
on a.id = b.id
and b.bowler like concat('%',a.bolwer_updated,'%')
and a.batting_team = b.batting_team
order by id,batting_team;

select * from t1
where id in ('23rd',
'35th',
'46th',
'50th',
'55th');

with c_t1 as(
select id,count(*) as c0
from t1
group by 1),
c_batsman as(
select id,count(*) as c1
from batsman
group by 1)
select a.id,b.id,a.c0,b.c1
from c_t1 as a
join 
c_batsman as b
on a.id=b.id
and c0 <> c1;

-- Extra runs

select * from extra_runs;

select id,runs,batting_team,
case when id = 'Qualifier 1 (N)' then 'Qualifier1 (N)'
when id = 'Qualifier 2 (N)' then 'Qualifier2 (N)'
when id = 'Eliminator (N)' then 'Eliminator'
when id = 'Final (N)' then 'Final'
else substring_index(id,' ',1) end as new_id
from extra_runs;

-- POTM

select * from potm;

drop function get_full_name;
DELIMITER //
CREATE FUNCTION get_full_name(name1 VARCHAR(255))
RETURNS VARCHAR(255)
DETERMINISTIC 
BEGIN
    DECLARE t_name VARCHAR(255);
    SET t_name = (SELECT CASE 
                    WHEN UPPER(name1) LIKE CONCAT('%', 'CSK', '%') THEN 'Chennai Super Kings'
                    WHEN UPPER(name1) LIKE CONCAT('%', 'RCB', '%') THEN 'Royal Challengers Bengaluru'
                    WHEN UPPER(name1) LIKE CONCAT('%', 'LSG', '%') THEN 'Lucknow Super Giants'
                    WHEN UPPER(name1) LIKE CONCAT('%', 'MI', '%') THEN 'Mumbai Indians'
                    WHEN UPPER(name1) LIKE CONCAT('%', 'GT', '%') THEN 'Gujarat Titans'
                    WHEN UPPER(name1) LIKE CONCAT('%', 'DC', '%') THEN 'Delhi Capitals'
                    WHEN UPPER(name1) LIKE CONCAT('%', 'PBKS', '%') THEN 'Punjab Kings'
                    WHEN UPPER(name1) LIKE CONCAT('%', 'RR', '%') THEN 'Rajasthan Royals'
                    WHEN UPPER(name1) LIKE CONCAT('%', 'SRH', '%') THEN 'Sunrisers Hyderabad'
                    WHEN UPPER(name1) LIKE CONCAT('%', 'KKR', '%') THEN 'Kolkata Knight Riders'
                    ELSE 'no' 
                  END);

    RETURN t_name;
END //

DELIMITER ;

select distinct id,player_name,team_name,
get_full_name(team_name),
case when id = 'Qualifier 1 (N)' then 'Qualifier1 (N)'
when id = 'Qualifier 2 (N)' then 'Qualifier2 (N)'
when id = 'Eliminator (N)' then 'Eliminator'
when id = 'Final (N)' then 'Final'
else substring_index(id,' ',1) end as new_id
from potm;

select * from batting_summarize;

select batsman,venue,sum(runs_scored) as total_runs, count(id_num) as no_of_matches,max(runs_scored) as higest_score_in_venue
from batting_summarize
group by 1,2;
