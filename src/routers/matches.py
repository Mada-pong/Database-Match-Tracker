from fastapi import APIRouter
from src.models.match_entry import MatchEntry

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/")
def create_match():
    return {"status": "ok"}

@router.post("/SubmitMatch")
def submit_text(data: MatchEntry):

    print(type(data))
    print(data.start_datetime)
    print(data.end_datetime)
    print(data.winning_side)
    
    return {"Status": "ok"}