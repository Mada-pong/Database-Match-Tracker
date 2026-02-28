from pydantic import BaseModel
from db.match_service import Side

class UserEntry(BaseModel):
    username: str
    
    pass

class PlayerEntry(BaseModel):
    player_id: int
    side: Side
    kills: int
    deaths: int
    assists: int

