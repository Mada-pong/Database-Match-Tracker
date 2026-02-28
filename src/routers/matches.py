from fastapi import APIRouter, Depends
from src.models.match_entry import MatchEntry
from db.match_service import getMatchByID, addMatch, addPlayerToMatch
from db.connection_service import get_connection
from mysql.connector import MySQLConnection

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/")
def get_match(matchID: int, conn: MySQLConnection = Depends(get_connection)):
    getMatchByID(conn, matchID)
    
    return {"status": "ok"}

@router.post("/SubmitMatch")
def create_match(data: MatchEntry, conn: MySQLConnection = Depends(get_connection)):

    print(type(data))
    print(data.start_datetime)
    print(data.end_datetime)
    print(data.winning_side)
    
    for player in data.player_list:
        print(player)
        
    print(get_connection())
    
        
    return {"Status": "ok"}