import json
from typing import List, Dict
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from src.chatbot.routes import router as chatbot_router
from src.auth.routes import router as auth_router
from src.schemas import CarInfo
from langchain.schema import Document
from src.config import configuration
from langchain.vectorstores import FAISS


def build_content(car: Dict[str, str | int]) -> str:
    content = [k + ": " + str(v) + "\n" for k, v in car.items()]
    return "".join(content)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    #embeddings = OpenAIEmbeddings(openai_api_key=configuration.openai_key)
    #with open("src/cars.json", "r") as f:
    #    cars = json.load(f)
    #    docs = [Document(page_content=build_content(c), metadata=c) for c in cars]
    #    db = FAISS.from_documents(docs, embeddings)
    #db.save_local("faiss_index")
    
    logging.info("Loading the ML model")
    logging.info("Loading the database")
    yield
    # Clean up the ML models and release the resources


app = FastAPI(title="Chatbot app", lifespan=lifespan)

app.include_router(chatbot_router, prefix="/chatbot", tags=["chatbot"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/cars/all", response_model=List[CarInfo])
def get_cars():
    print(os.getcwd())
    print(os.listdir())
    with open("src/cars.json", "r") as f:
        cars = json.loads(f.read())
    return cars
