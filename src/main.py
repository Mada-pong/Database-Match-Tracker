from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}

class UserInput(BaseModel):
    text: str 

@app.post("/submit")
def submit_text(data: UserInput):
    print(type(data))
    print(data.text)
    return {"you_sent": data.text}