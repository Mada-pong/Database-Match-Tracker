from fastapi import APIRouter, Depends
from src.models import AddPlayer, GetPlayer
from db.players_service import showSpecificPlayer, deletePlayerSoft, addPlayer, showAllPlayers, changeActiveStatusesOfAll, restorePlayer, getUserStatus
from db.connection_service import get_connection
from mysql.connector import MySQLConnection


router = APIRouter(prefix="/players", tags=["players"])


@router.post("/ChangeAllStatusesOfActive")
def change_all_statues_of_active(conn: MySQLConnection = Depends(get_connection)):
    player_data = changeActiveStatusesOfAll(conn)
    return { "status": "ok",
            "data": player_data}


@router.get("/GetPlayerByUsername")
def get_player_by_username(player_username: str, conn: MySQLConnection = Depends(get_connection)):
    player_data = showSpecificPlayer(player_username, conn)
    return {"status": "ok",
            "data": player_data}
    
@router.get("/GetPlayerStatus")
def get_player_status_by_ID(id: int, conn: MySQLConnection = Depends(get_connection)):
    player_data = getUserStatus(id, conn)
    return {"status": "ok",
            "data": player_data}

    
@router.post("/DeletePlayerSoft")
def delete_player_by_ID(id: int, conn: MySQLConnection = Depends(get_connection)):
    player_data = deletePlayerSoft(id, conn)
    
    return {"status": "ok",
            "data": player_data}

@router.post("/RestorePlayer")
def restore_player_by_ID(id: int, conn: MySQLConnection = Depends(get_connection)):
    player_data = restorePlayer(id, conn)
    
    return {"status": "ok",
            "data": player_data}


@router.post("/AddPlayer")
def add_player(data: AddPlayer.AddPlayer, conn: MySQLConnection = Depends(get_connection)):
    player_data = addPlayer(data.username, data.email, data.dob, conn)
    return {"status": "ok",
            "data": player_data}
    
    
@router.post("/PostAllPlayers")
def get_all_players(conn: MySQLConnection = Depends(get_connection)):
    player_data = showAllPlayers(conn)
    return { "status": "ok",
            "data": player_data}