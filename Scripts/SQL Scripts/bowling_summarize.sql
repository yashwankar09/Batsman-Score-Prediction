select * from bowler;

create table bowling_summarize as
with potm_1 as (
select distinct player_name,
get_full_name(team_name) as team,
case when id = 'Qualifier 1 (N)' then 'Qualifier1 (N)'
when id = 'Qualifier 2 (N)' then 'Qualifier2 (N)'
when id = 'Eliminator (N)' then 'Eliminator'
when id = 'Final (N)' then 'Final'
else substring_index(id,' ',1) end as new_id
from potm)
select a.*,b.player_name as potm,CREATE_ID(a.id) as id_num,str_to_date(CREATE_DATES(a.match_date), '%M-%d-%YYYY') as new_date
from bowler a
left join 
potm_1 b
on a.id = b.new_id and (a.bowling_team = b.team or a.batting_team = b.team);

select * from bowling_summarize;