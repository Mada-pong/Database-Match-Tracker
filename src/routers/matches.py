from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(prefix="/matches", tags=["matches"])

class UserInput(BaseModel):
    text: str 

@router.post("/")
def create_match():
    return {"status": "ok"}

@router.post("/submit")
def submit_text(data: UserInput):
    print(type(data))
    print(data.text)
    return {"you_sent": data.text}