DELIMITER $$

create trigger after_insert_match_player
after insert on match_player 
for each row
begin 
	update overall_stats
    set kills = kills + NEW.kills, 
		deaths = deaths + NEW.deaths,
        assists = assists + NEW.assists,
        total_games_played = total_games_played + 1
	where statsID = NEW.playerID; 
end $$ 

DELIMITER ;

DELIMITER $$

create trigger after_insert_player_profile
after insert on player_profile
for each row 
begin 
	Insert overall_stats 
    values (NEW.playerID, 0, 0, 0, 0);
end $$

DELIMITER ;