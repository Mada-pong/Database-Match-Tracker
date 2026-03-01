from pydantic import BaseModel
from datetime import date


class GetPlayer(BaseModel):
    playerID: int
    username: str
    email: str
    dob: date
