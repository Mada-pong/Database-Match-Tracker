from fastapi import APIRouter, Depends
from src.models.match_entry import MatchEntry
from db.match_service import getMatchByID, addMatch, addPlayerToMatch, Side
from db.connection_service import get_connection
from mysql.connector import MySQLConnection

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/")
def get_match(matchID: int, conn: MySQLConnection = Depends(get_connection)):
    match_data = getMatchByID(conn, matchID)
    
    return {"status": "ok",
            "data": match_data}

@router.post("/SubmitMatch")
def create_match(data: MatchEntry, conn: MySQLConnection = Depends(get_connection)):
    new_matchID = addMatch(conn, data.start_datetime, data.end_datetime, data.winning_side)
    
    for player in data.player_list:
        addPlayerToMatch(conn, new_matchID, player.player_id, player.side, player.kills, player.deaths, player.assists)
        
    return {"Status": "ok"}
