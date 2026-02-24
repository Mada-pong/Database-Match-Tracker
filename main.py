import test_db as tb
import QueriesModule as QM
import os
import dotenv
import mysql.connector


def menuPrompt():
    print("Hello, welcome to the player data tracker. Please choose one of the following:\n" \
    "1. List all players\n" \
    "2. Add Match to player\n" \
    "3. Look at specific player\n"\
    "4. Test connection"
    )
            
            
            



def main():
    running = True
    #print("CWD:", os.getcwd())
    env_path = dotenv.find_dotenv(usecwd=True)
    print("find_dotenv:", repr(env_path))

    """while (running):
        menuPrompt()
        userInput = input()
        match(userInput):
            case("1"):
                break
            case("2"):
                
                break
            
            case("3"):
                
                break
            case("4"):
                tb.testConnection()
                break
"""

if __name__ == "__main__":
    main()



