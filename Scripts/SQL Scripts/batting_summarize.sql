drop table batting_summarize;
create table batting_summarize as

with temp1 as (
select distinct(id) as id,wicket_by,
case when id not in ('Qualifier1 (N)','Final','Qualifier2 (N)','Eliminator') then regexp_replace(id,'[^0-9]','')
when id = 'Qualifier1 (N)' then 71
when id = 'Qualifier2 (N)' then 73
when id = 'Eliminator' then 72
when id = 'Final' then 74
else id end as id_num,
case when wicket_by = 'Kumar' and bowling_team = 'Sunrisers Hyderabad' then 'Bhuvneshwar Kumar'
else wicket_by end as bowler_new
from
batsman),

extra_r as(
select id,runs,batting_team,
case when id = 'Qualifier 1 (N)' then 'Qualifier1 (N)'
when id = 'Qualifier 2 (N)' then 'Qualifier2 (N)'
when id = 'Eliminator (N)' then 'Eliminator'
when id = 'Final (N)' then 'Final'
else substring_index(id,' ',1) end as new_id
from extra_runs),

potm_1 as (
select distinct player_name,
get_full_name(team_name) as team,
case when id = 'Qualifier 1 (N)' then 'Qualifier1 (N)'
when id = 'Qualifier 2 (N)' then 'Qualifier2 (N)'
when id = 'Eliminator (N)' then 'Eliminator'
when id = 'Final (N)' then 'Final'
else substring_index(id,' ',1) end as new_id
from potm)

select a.*,cast(t1.id_num as signed integer) as id_num,
coalesce(b.bowler,'-') as bowler,ex.runs as extra_runs,ptm.player_name as potm, 
str_to_date(CREATE_DATES(a.match_date), '%M-%d-%YYYY') as new_date
from batsman a
left join
temp1 as t1
on a.id = t1.id
and a.wicket_by = t1.wicket_by
left join
bowler b
on b.id = a.id and b.batting_team = a.batting_team
and b.id = t1.id and b.bowler like concat('%',t1.bowler_new,'%')
left join
extra_r ex
on a.id = ex.new_id and a.batting_team = ex.batting_team
left join
potm_1 as ptm
on a.id = ptm.new_id and (a.batting_team = ptm.team or a.bowling_team = ptm.team)
order by cast(t1.id_num as signed)  desc;