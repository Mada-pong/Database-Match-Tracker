from fastapi import APIRouter

router = APIRouter(prefix="/matches", tags=["matches"])

@router.post("/")
def create_match():
    return {"status": "ok"}