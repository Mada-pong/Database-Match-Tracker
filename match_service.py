from mysql.connector.connection import MySQLConnection
from mysql.connector import Error as MySQLError
from enum import Enum

from connection_service import startConnection

class Side(Enum):
    RED = 1 
    BLUE = 2

### Add a match and returns the match ID for later use. 
def addMatch(conn: MySQLConnection, start_datetime: str, end_datetime: str, winning_side: Side):
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

def addPlayerToMatch(conn: MySQLConnection, matchID: int, playerID: int, side: Side, kills: int, deaths: int, assists: int):
    cur = conn.cursor()
    
    insertSQL = """
    insert into match_player 
    values (%s, %s, %s, %s, %s, %s)
    """
    args = (matchID, playerID, side, kills, deaths, assists)
    
    try: 
        cur.execute(insertSQL, args)
        conn.commit()
    except MySQLError as error:
        print(f"Error during insert: {error}")
        conn.rollback()
    finally:
        cur.close()

#Debug
# connection = startConnection()