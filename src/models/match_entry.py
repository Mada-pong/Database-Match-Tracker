from pydantic import BaseModel
from datetime import datetime
from db.match_service import Side

class MatchEntry(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
    winning_side: Side
