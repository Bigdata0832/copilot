from fastapi import FastAPI
from pydantic import BaseModel
from src.utils.assistant import hello

app = FastAPI()

class Name(BaseModel):
    name: str

@app.post("/greet/")
async def greet(name: Name):
    return {"message": hello(name.name)}


# test to -> http://127.0.0.1:8000/docs