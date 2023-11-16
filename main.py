import json
from typing import List
from fastapi import FastAPI

from chatbot.routes import router as chatbot_router

from chatbot.schemas import Message
from schemas import CarInfo

from config import configuration

app = FastAPI(title="Chatbot app")

app.include_router(chatbot_router, prefix="/chatbot", tags=["chatbot"])


@app.get("/cars/all", response_model=List[CarInfo])
def get_cars():
    with open("cars.json", "r") as f:
        cars = json.loads(f.read())
    return cars
