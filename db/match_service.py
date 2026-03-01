from mysql.connector.connection import MySQLConnection
from mysql.connector import Error as MySQLError
from enum import Enum
from datetime import datetime

class Side(Enum):
    RED = 1 
    BLUE = 2

def get_match_by_ID(matchID: int, conn: MySQLConnection) -> dict:
    cur = conn.cursor(dictionary=True)
    
    selectSQL = """
    select * from match_data
    where matchID = %s;
    """
    
    args = (matchID,)
    
    try:
        cur.execute(selectSQL, args)
        row = cur.fetchone()
        
        row["duration_min"] = get_match_duration_min(row["start_datetime"], row["end_datetime"])
        return row
    except MySQLError as error: 
        print(f"MYSQL ERROR: \n {error}")
    finally:
        cur.close()
        
## Format datetime into float and convert it nicely into minutes
def get_match_duration_min(start_datetime: datetime, end_datetime: datetime) -> float:
    seconds = (end_datetime - start_datetime).total_seconds()
    minutes = round(seconds / 60, 2)
    
    return minutes
    
def get_match_related_player_by_ID(matchID: int, conn: MySQLConnection):
    cur = conn.cursor(dictionary=True)
    
    selectSQL = """
    select player_profile.playerID, 
    CASE 
        WHEN player_profile.isActive = FALSE THEN 'null'
        ELSE player_profile.username
    END AS username,
    CASE
        when player_profile.isActive = FALSE then "False"
        else "True"
    END AS isActive,
    side, kills, deaths, assists from match_player 
    left join player_profile
    on match_player.playerID = player_profile.playerID
    where match_player.matchID = %s
    order by side asc;
    """
    
    args = (matchID,)
    
    try: 
        cur.execute(selectSQL, args)
        rows = cur.fetchall()
        return rows
    except MySQLError as error:
        print(f"MYSQL ERROR: \n {error}")
    finally:
        cur.close()
    
def get_total_kills_in_match(matchID: int, conn: MySQLConnection):
    cur = conn.cursor(dictionary=True)
    
    selectSQL = """
    select Side as side, sum(kills) as total_kills from match_player 
    left join player_profile
    on match_player.playerID = player_profile.playerID
    where match_player.matchID = %s
    group by side;
    """
    
    args = (matchID,)
    total_kills_data = {"Blue": 0,
                        "Red": 0}
    
    try:
        cur.execute(selectSQL, args)
        rows = cur.fetchall()
        
        if (len(rows) != 0):
            total_kills_data["Blue"] = rows[0]["total_kills"]
            total_kills_data["Red"] = rows[1]["total_kills"]
            
        
        return total_kills_data
    except MySQLConnection as error:
        print(f"MYSQL ERROR: \n {error}")
    finally:
        cur.close()
    
### Add a match and returns the match ID for later use. 
def add_match(start_datetime: str, end_datetime: str, winning_side: Side, conn: MySQLConnection) -> int:
    cur = conn.cursor()
    args = (start_datetime, end_datetime, winning_side.name.capitalize(), 0)
    matchID = -1
    
    try: 
        results = cur.callproc("add_match_entry", args)
        matchID = results[3]
        conn.commit()
    except MySQLError as error: 
        print(f"MYSQL ERROR: \n {error}")
        conn.rollback()
    finally:
        cur.close()
        
    return matchID

def add_player_to_match(matchID: int, playerID: int, side: Side, kills: int, deaths: int, assists: int, conn: MySQLConnection):
    cur = conn.cursor()
    
    insertSQL = """
    insert into match_player 
    values (%s, %s, %s, %s, %s, %s)
    """
    args = (matchID, playerID, side.name.capitalize(), kills, deaths, assists)
    
    try: 
        cur.execute(insertSQL, args)
        conn.commit()
    except MySQLError as error:
        print(f"Error during insert: {error}")
        conn.rollback()
    finally:
        cur.close()
