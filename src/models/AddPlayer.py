from pydantic import BaseModel
from datetime import date


class AddPlayer(BaseModel):
    username: str
    email: str
    dob: date
