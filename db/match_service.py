from mysql.connector.connection import MySQLConnection
from mysql.connector import Error as MySQLError
from enum import Enum

class Side(Enum):
    RED = 1 
    BLUE = 2

def get_Match_By_ID(matchID: int, conn: MySQLConnection) -> dict:
    cur = conn.cursor(dictionary=True)
    
    selectSQL = """
    select * from match_data
    where matchID = %s;
    """
    
    args = (matchID,)
    
    try:
        cur.execute(selectSQL, args)
        row = cur.fetchone()
        return row
    except MySQLError as error: 
        print(f"MYSQL ERROR: \n {error}")
    finally:
        cur.close()
        
def get_Match_Related_Player_By_ID(matchID: int, conn: MySQLConnection):
    cur = conn.cursor(dictionary=True)
    
    selectSQL = """
    select player_profile.playerID, 
    CASE 
        WHEN player_profile.isActive = FALSE THEN 'Inactive'
        ELSE player_profile.username
    END AS username, 
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
        

### Add a match and returns the match ID for later use. 
def add_Match(start_datetime: str, end_datetime: str, winning_side: Side, conn: MySQLConnection) -> int:
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

def add_Player_To_Match(matchID: int, playerID: int, side: Side, kills: int, deaths: int, assists: int, conn: MySQLConnection):
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

