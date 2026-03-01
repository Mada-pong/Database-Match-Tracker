from fastapi import FastAPI
from src.routers import matches, players



app = FastAPI()
app.include_router(matches.router)
app.include_router(players.router)

@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}



