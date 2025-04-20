-- create new date
drop function CREATE_DATES;
DELIMITER //
CREATE FUNCTION CREATE_DATES(DATE_COL VARCHAR(255))
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
	DECLARE new_date varchar(255);
    set new_date = (
    concat_ws('-',substring_index(trim(substring_index(DATE_COL,'/',1)),' ',1),
	substring_index(substring_index(substring_index(trim(substring_index(DATE_COL,'/',2)),' ',2),'/',-1),' ',-1),
	substring_index(trim(substring_index(DATE_COL,'/',-1)),' ',-1))
    );
    return new_date;
END//
DELIMITER //;

-- getting full team from abbrivations.

drop function get_full_name;
DELIMITER //
CREATE FUNCTION get_full_name(name1 VARCHAR(255))
RETURNS VARCHAR(255)
DETERMINISTIC 
BEGIN
    DECLARE t_name VARCHAR(255);
    SET t_name = (SELECT CASE 
                    WHEN UPPER(name1) LIKE CONCAT('%', 'CSK', '%') THEN 'Chennai Super Kings'
                    WHEN UPPER(name1) LIKE CONCAT('%', 'RCB', '%') THEN 'Royal Challengers Bangalore'
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

-- create new id_num col

DELIMITER //
CREATE FUNCTION CREATE_ID(ID_COL VARCHAR(255))
RETURNS INTEGER(20)
DETERMINISTIC
BEGIN
	DECLARE id_new integer(20);
    set id_new = (
    select 
	case when ID_COL not in ('Qualifier1 (N)','Final','Qualifier2 (N)','Eliminator') then regexp_replace(ID_COL,'[^0-9]','')
	when ID_COL = 'Qualifier1 (N)' then 71
	when ID_COL = 'Qualifier2 (N)' then 73
	when ID_COL = 'Eliminator' then 72
	when ID_COL = 'Final' then 74
	else ID_COL end
    );
    return id_new;
END //
DELIMITER ;

drop function GET_NO_RESULTS_POINTS;
DELIMITER //
CREATE FUNCTION GET_NO_RESULTS_POINTS(TEAM_NAME VARCHAR(255))
RETURNS INTEGER(20)
DETERMINISTIC
BEGIN
	DECLARE pt INTEGER(20);
    set pt = (
    select count(distinct id) from batsman
    where (summary = '-' or summary = 'No result') and batting_team = TEAM_NAME
    );
    return pt;
END //
DELIMITER ;
