import os
import dotenv
import mysql.connector




def testConnection():
    # TEST IF THE CONNECTION TO THE DATABASE IS POSSIBLE 
    # CREDENTIALS SHOULD BE PLACED UNDER THE FILE .env
    #
    # DB_HOST=host
    # DB_PORT=port
    # DB_USER=username
    # DB_PASSWORD=password
    # DB_NAME=database

    print("CWD:", os.getcwd())

    env_path = dotenv.find_dotenv(usecwd=True)
    print("find_dotenv:", repr(env_path))

    loaded = dotenv.load_dotenv(env_path, override=True)
    print("load_dotenv loaded:", loaded)

    print("DB_HOST =", repr(os.getenv("DB_HOST")))
    print("DB_PORT =", repr(os.getenv("DB_PORT")))
    print("DB_USER =", repr(os.getenv("DB_USER")))

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=repr(os.getenv("DB_USER")),
        password=os.getenv("DB_PASSWORD"),
    )
    
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    print("MySQL version:", cursor.fetchone()[0])
    cursor.close()
    print("Connected:", connection.is_connected())
    connection.close()
