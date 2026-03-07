from mysql.connector.connection import MySQLConnection
from mysql.connector import Error as MySQLError
from datetime import date




def changeActiveStatusesOfAll(conn: MySQLConnection):
    updateSQL = """
    UPDATE player_profile p
    SET isActive = EXISTS (
        SELECT 1
        FROM match_player m 
        WHERE m.playerID = p.playerID
    );
    """
    
    selectSQL = """
    SELECT * FROM player_profile
    
    """
    cur = conn.cursor(dictionary=True)
    
    try:
        cur.execute(updateSQL)
        conn.commit()
        
        cur.execute(selectSQL)
        
        return cur.fetchall()        
    except MySQLError as error:
        print(f"MYSQL ERROR: \n {error}")
    finally:
        cur.close()
        
    return

def showSpecificPlayer(username: str, conn: MySQLConnection,):
    selectSQL = """
    select playerID, username, total_games_played, kills, deaths, assists from player_profile 
    left join overall_stats
    on player_profile.playerID = overall_stats.statsID
    where player_profile.username = %s;
    """
    
    cur = conn.cursor(dictionary=True)
    try: 
        cur.execute(selectSQL, (username,))
        row = cur.fetchone()
        return row 
    except MySQLError as error: 
        print(f"MYSQL ERROR: \n {error}")
    finally:
        cur.close()
        
    return

def getUserStatus(player_id: int, conn: MySQLConnection):
    selectSQL = """
    select * from player_profile
    where playerID = %s
    """
    
    args = (player_id, )
    cur = conn.cursor(dictionary=True)
    
    try: 
        cur.execute(selectSQL, args)
        
        row = cur.fetchone()

        if row is None:
            return -1

        player_data = {
            "playerID": player_id,
            "isActive": row["isActive"]
        }

        return player_data
    except MySQLError as error:
        print(f"Error during insert {error}")
    finally:
        cur.close()
        
        
def deletePlayerHard(player_id: int, conn:MySQLConnection) -> None:
    selectSQL = """
    SELECT * FROM player_profile
    WHERE playerID = %s
    """
    
    
    deleteSQL = """
    DELETE FROM player_profile
    WHERE playerID = %s
    """
    args = (player_id, )
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(selectSQL, args)
        if cur.rowcount == 0:
            print(f"User ({player_id}) does not exist or is already marked as inactive")
        else:
            print(f"User ({player_id}) will be deleted")
            
        player_data = cur.fetchone()
        cur.execute(deleteSQL, args)
        conn.commit()
        return player_data
    
    except MySQLError as error:
        conn.rollback()
        print(f"Error during insert {error}")
        raise
    finally:
        cur.close()
    
    
    
        


def deletePlayerSoft(player_id: int, conn: MySQLConnection) -> None:
    updateSQL = """
    UPDATE player_profile p
    SET isActive = 0
    WHERE playerID = %s
    """
    
    selectSQL = """
    select * from player_profile
    where playerID = %s
    """

    args = (player_id,)
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute(updateSQL, args)
        conn.commit()

        if cur.rowcount == 0:
            print(f"User ({player_id}) does not exist or is already marked as inactive")
        else:
            print(f"User ({player_id}) has been deleted successfully")
            
        cur.execute(selectSQL, args)
        player_data_row = cur.fetchone()
            
        return player_data_row
    except MySQLError as error:
        conn.rollback()
        print(f"Error during insert {error}")
        raise 
    finally:
        cur.close()

def restorePlayer(player_id: int, conn: MySQLConnection):
    updateSQL = """
    UPDATE player_profile p
    SET isActive = 1
    WHERE playerID = %s
    """
    
    cur = conn.cursor(dictionary=True)
    args = (player_id,)
    
    try:
        cur.execute(updateSQL, args)
        conn.commit()

        if cur.rowcount == 0:
            return f"User ID ({player_id}) was not found."
        else:
            return f"User ID ({player_id}) restored successfully."
    except MySQLError as error:
        conn.rollback()
        print(f"Error during insert {error}")
        raise
    finally:
        cur.close()
        
def addPlayer(username: str, email: str, dob: date, conn: MySQLConnection):

    
    if not username:
        print("Username invalid")
        return 0
    if not email:
        print("Email invalid")
        return 0
    if not dob:
        print("Date of Birth invalid")
        return 0

    insertSQL = """
    INSERT INTO player_profile (username, email, dob, isActive)
    VALUES (%s, %s, %s, %s)
    """

    selectSQL = """
    SELECT playerID, username, email, dob
    FROM player_profile
    WHERE playerID = %s
    """

    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(insertSQL, (username, email, dob, 1))
        createdID = cur.lastrowid
        conn.commit()

        cur.execute(selectSQL, (createdID,))
        row = cur.fetchone()
        return row
    except MySQLError as error:
        conn.rollback()
        print(f"Error during insert: {error}")
        raise
    finally:
        cur.close()


def showAllPlayers(conn: MySQLConnection):

    sql = """
    SELECT *
    FROM player_profile
    """
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    except MySQLError as error:
        print(error)

    finally:
        cur.close()

    return