import test_db as tb
import QueriesModule as QM
import os
import dotenv
import mysql.connector as CON


def menuPrompt():
    print(
        "Hello, welcome to the player data tracker. Please choose one of the following:\n"
        "1. List all players\n"
        "2. Add player\n"
        "3. Look at specific player (by username)\n"
        "4. Delete specific player\n"
        "5. Test connection\n"
        "6. Quit"
    )


def startConnection():
    dotenv.load_dotenv()
    if not os.getenv("DB_HOST"):
        raise RuntimeError("DB_HOST is missing in env file or not reached")
    return CON.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def main():
    running = True
    conn = startConnection()

    while running:
        menuPrompt()
        userInput = input()
        match userInput:
            case "1":
                QM.showAllPlayers(conn)
            case "2":
                addedPlayer = QM.addPlayer(conn)
                if addedPlayer is not None:
                    print(
                        f"username {addedPlayer['username']}, email {addedPlayer['email']}, dob {addedPlayer['dob']}"
                    )
            case "3":
                username = input("Choose player username ").strip()
                row = QM.showSpecificPlayer(conn, username)
                
                print(
                    f"Username: {row['username']}\n"
                    f"kills: {row['kills']}\n"
                    f"deaths: {row['deaths']}\n"
                    f"assists: {row['assists']}\n"
                )
            case "4":
                QM.deletePlayer(conn)
            case "5":
                tb.testConnection()
            case "6":
                running = False

    conn.close()


if __name__ == "__main__":
    main()
