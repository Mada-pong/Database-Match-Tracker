use matchdb;

create table player_profile (
	playerID int primary key auto_increment,
    username varchar(50) not null,
    email varchar(200) not null,
    dob date not null
);

create table overall_stats (
	statsID int primary key,
    total_games_played int not null,
    kills int not null,
    deaths int not null,
    assists int not null,
    foreign key (statsID) references player_profile(playerID)
);

create table match_profile (
	matchID int primary key auto_increment, 
    start_datetime datetime not null, 
    end_datetime datetime not null
);

create table match_player (
	matchID int not null,
	playerID int not null,
    side varchar(20) not null,
    kills int not null,
    deaths int not null,
    assists int not null,
    
    primary key (matchID, playerID),
    foreign key (matchID) references match_profile(matchID),
    foreign key (playerID) references player_profile(playerID)
);


