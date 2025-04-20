create table points_table as
with cte0 as(
select batting_team as exb,sum(runs) as runs
from extra_runs
where id not in ('Qualifier1 (N)','Final','Qualifier2 (N)','Eliminator')
group by 1),
-- 141
cte1 as (
select batting_team,sum(runs_scored)+max(cz.runs) as runs_scored,sum(balls_played)/6 as overs
from batsman a
left join cte0 as cz
on a.batting_team=cz.exb
where id not in ('Qualifier1 (N)','Final','Qualifier2 (N)','Eliminator')
group by 1),
-- Royal Challengers Bengaluru	2789	289.0000
cte2 as (
select bowling_team,sum(overs) as overs_bowled,sum(runs) as runs_conceded
from bowler
where id not in ('Qualifier1 (N)','Final','Qualifier2 (N)','Eliminator')
group by 1),
cte3 as(
select a.batting_team,(a.runs_scored/a.overs) - (b.runs_conceded/b.overs_bowled) as NRR
from cte1 a
join cte2 b
on a.batting_team=b.bowling_team),
win_c as(
select winner,count(distinct id) as wins,
case when winner = 'Royal Challengers Bangalore' then 'Royal Challengers Bengaluru'
else winner end as team
from batsman
where id not in ('Qualifier1 (N)','Final','Qualifier2 (N)','Eliminator')
group by 1
order by count(distinct id) desc)
select a.batting_team,count(distinct id) as matches,c.wins,(count(distinct id)-c.wins-sum(case when summary = '-' then 1 else 0 end)) as lose,
sum(case when summary = '-' then 1 else 0 end) as NR,
max(c.wins) * 2 + sum(case when summary = '-' then 1 else 0 end) as points,round(max(ct3.NRR),3) as NRR
from batsman a
left join
win_c as c
on a.batting_team = c.team
left join cte3 ct3
on a.batting_team=ct3.batting_team
where id not in ('Qualifier1 (N)','Final','Qualifier2 (N)','Eliminator')
group by 1,3
order by wins desc ,max(ct3.NRR) desc;

select * from points_table;