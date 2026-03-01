from fastapi import APIRouter, Depends
from src.models.match_entry import MatchEntry
from db.match_service import get_match_by_ID, add_match, add_player_to_match, Side, get_match_related_player_by_ID, get_total_kills_in_match
from db.connection_service import get_connection
from mysql.connector import MySQLConnection

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/")
def get_match(matchID: int, conn: MySQLConnection = Depends(get_connection)):
    match_data = get_match_by_ID(matchID, conn)
    total_kills_data = get_total_kills_in_match(matchID=matchID, conn=conn)
    player_match_data = get_match_related_player_by_ID(matchID=matchID, conn=conn)
    
    return {"status": "ok",
            "match_data": match_data,
            "total_kills": total_kills_data,
            "player_data": player_match_data}

@router.post("/SubmitMatch")
def create_match(data: MatchEntry, conn: MySQLConnection = Depends(get_connection)):
    new_matchID = add_match(data.start_datetime, data.end_datetime, data.winning_side, conn)
    
    for player in data.player_list:
        add_player_to_match(new_matchID, player.player_id, player.side, player.kills, player.deaths, player.assists, conn)
        
    return {"Status": "ok"}
