DROP PROCEDURE IF EXISTS matchdb.add_match_entry;

DELIMITER $$

create procedure add_match_entry(IN p_start_datetime datetime, IN p_end_datetime datetime, IN p_winning_side varchar(5))
Begin
	start transaction; 
    
	IF p_start_datetime >= p_end_datetime THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Start must be before end';
    END IF; 
    
    insert into match_data (start_datetime, end_datetime, winning_side)
    values (p_start_datetime, p_end_datetime, p_winning_side);
    
    commit;
end $$

DELIMITER ; 
