from fastapi import APIRouter, FastAPI
import uuid
import json
from fastapi.exceptions import HTTPException
from src.chatbot.schemas import Conversation, ChatMessage
from src.schemas import OpenaiConfig
from src.config import configuration
from src.chatbot.service import QaService
from src.chatbot.utils import init_tools


router = APIRouter()

chats = {}
tools = init_tools()


@router.get("/chat", response_model=Conversation)
async def get_messages(chat_id: str):
    messages = chats.get(chat_id)
    try:
        return Conversation(messages=messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No chat found with id {chat_id}")


@router.post("/chat", response_model=ChatMessage)
async def chat(message: ChatMessage):
    user = message.chat_user if message.chat_user else str(uuid.uuid4())
    query = message.message

    openai_config = OpenaiConfig(
        openai_key=configuration.openai_key,
        chat_model_version=configuration.chat_model_version,
    )
    qa = QaService(openai_config=openai_config)

    with open("src/cars.json", "r") as f:
        cars = json.load(f)

    formatted_json = json.dumps(cars, indent=2)

    prompt = f"""Ti verranno fornite la lista delle macchine disponibili in un concessionario. 
Quando proponi una macchina al cliente descrivigli alcune caratteristiche ed allega sempre il link dell'auto.
Questa è la lista delle macchine:
{formatted_json}
    """
    if chats.get(user):
        agent = chats.get(user)
    else:
        agent = qa.init_agent(tools=tools)

    ## TODO save messages somewhere

    response = agent.invoke({"input": f"{prompt}.\n\n Cliente: {query}"})["output"]
    return ChatMessage(**{"sender": "AI", "message": response, "chat_user": user})
