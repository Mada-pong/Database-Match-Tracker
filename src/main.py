from fastapi import FastAPI
from src.routers import matches

app = FastAPI()
app.include_router(matches.router)

@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}
