from fastapi import APIRouter, Depends
from src.models.match_entry import MatchEntry
from db.match_service import get_Match_By_ID, add_Match, add_Player_To_Match, Side, get_Match_Related_Player_By_ID
from db.connection_service import get_connection
from mysql.connector import MySQLConnection

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/")
def get_match(matchID: int, conn: MySQLConnection = Depends(get_connection)):
    match_data = get_Match_By_ID(matchID, conn)
    player_match_data = get_Match_Related_Player_By_ID(matchID=matchID, conn=conn)
    
    return {"status": "ok",
            "match_data": match_data,
            "player_data": player_match_data}

@router.post("/SubmitMatch")
def create_match(data: MatchEntry, conn: MySQLConnection = Depends(get_connection)):
    new_matchID = add_Match(data.start_datetime, data.end_datetime, data.winning_side, conn)
    
    for player in data.player_list:
        add_Player_To_Match(new_matchID, player.player_id, player.side, player.kills, player.deaths, player.assists, conn)
        
    return {"Status": "ok"}
