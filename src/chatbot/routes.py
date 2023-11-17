from fastapi import APIRouter
from src.chatbot.schemas import Message, Conversation
from src.schemas import OpenaiConfig
from src.config import configuration
from src.chatbot.service import QaService

import json

router = APIRouter()


@router.get("/chat", response_model=Conversation)
async def get_messages():
    return Conversation(
        **{"messages": [Message(**{"sender": "test", "message": "test"})]}
    )


@router.post("/chat", response_model=Message)
async def chat(message: Message):
    user = message.sender
    query = message.message

    openai_config = OpenaiConfig(
        openai_key=configuration.openai_key,
        chat_model_version=configuration.chat_model_version,
    )
    qa = QaService(openai_config=openai_config)

    with open("src/cars.json", "r") as f:
        cars = json.loads(f.read())

    prompt = f"""Ti verranno fornite la lista delle macchine disponibili in un concessionario. 
    Il tuo compito è servire i clienti per le domande riguardanti il concessionario.
    Questa è la lista delle macchine:
    {str(cars)}
    """

    response = await qa.basic_answer(query, prompt)

    return {"sender": "AI", "message": response}
