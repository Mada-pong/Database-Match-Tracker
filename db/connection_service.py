import os
import dotenv
import mysql.connector as connection
from mysql.connector import MySQLConnection

def startConnection() -> MySQLConnection:
    dotenv.load_dotenv()
    if not os.getenv("DB_HOST"):
        raise RuntimeError("DB_HOST is missing in env file or not reached")
    return connection.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    
def get_connection() -> MySQLConnection:
    connection = startConnection()
    
    try:
        yield connection
    finally:
        connection.close()