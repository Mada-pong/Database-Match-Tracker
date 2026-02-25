from mysql.connector.connection import MySQLConnection
from mysql.connector import Error as MySQLError

def deletePlayer(conn: MySQLConnection) -> None:
    player_id = int(input("Choose id of player to delete ").strip())

    selectSQL = """
    SELECT *
    FROM player_profile
    WHERE playerID = %s
    """

    deleteSQL = """
    DELETE FROM player_profile
    WHERE playerID = %s
    """

    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(selectSQL, (player_id,))
        row = cur.fetchone()
        if row is None:
            print("No matching player found")
            return
        choice = input(
            f"You are about to delete following player from database: {row['username']}. Proceed? Y/N "
        ).upper()
        if choice != "Y":
            print("Delete cancelled")
            return

        cur.execute(deleteSQL, (player_id,))
        conn.commit()

        if cur.rowcount == 0:
            print("Player was not deleted (no longer existed)")
        else:
            print("Player deletion successful")

    except MySQLError as error:
        conn.rollback()
        print(f"Error during insert {error}")
        raise
    finally:
        cur.close()


def addPlayer(conn: MySQLConnection):

    username = input("Choose player username ").strip()
    email = input("Input player email ").strip()
    dob = input("Input player dob YYYY-MM-DD ").strip()
    choice = input(
        f"{username}, {email}, {dob} about to be added, proceed (Y/N)?"
    ).upper()
    if choice != "Y":
        print("Aborting...")
        return
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
    INSERT INTO player_profile (username, email, dob)
    VALUES (%s, %s, %s)
    """

    selectSQL = """
    SELECT playerID, username, email, dob
    FROM player_profile
    WHERE playerID = %s
    """

    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(insertSQL, (username, email, dob))
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
        for row in rows:
            print(f"ID: {row['playerID']} username: {row['username']}")

    except MySQLError as error:
        print(error)

    finally:
        cur.close()

    return

def showSpecificPlayer(conn: MySQLConnection, username: str):
    selectSQL = """
    select username, total_games_played, kills, deaths, assists from player_profile 
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

def getIDByUsername(conn: MySQLConnection, username: str):
    selectSQL = """
    select playerID from player_profile
    where username = %s;
    """
    
    cur = conn.cursor()
    
    try: 
        cur.execute(selectSQL, (username,))
        row = cur.fetchone()
        return row[0]
    except MySQLError as error:
        print(f"MYSQL ERROR: \n {error}")
    finally:
        cur.close()
        
    return -1