import json
from typing import List
from fastapi import FastAPI
import os

from src.chatbot.routes import router as chatbot_router

from src.chatbot.schemas import Message
from src.schemas import CarInfo

from src.config import configuration

app = FastAPI(title="Chatbot app")

app.include_router(chatbot_router, prefix="/chatbot", tags=["chatbot"])


@app.get("/cars/all", response_model=List[CarInfo])
def get_cars():
    print(os.getcwd())
    print(os.listdir())
    with open("src/cars.json", "r") as f:
        cars = json.loads(f.read())
    return cars
