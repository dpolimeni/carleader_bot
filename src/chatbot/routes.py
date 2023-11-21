from fastapi import APIRouter, FastAPI
import uuid
import json
from fastapi.exceptions import HTTPException
from src.chatbot.schemas import Conversation, ChatMessage, Message
from src.schemas import OpenaiConfig
from src.config import configuration
from src.chatbot.service import QaService
from src.chatbot.utils import init_tools


router = APIRouter()

agents = {}
chats = {}
tools = init_tools()


@router.get("/chat", response_model=Conversation)
async def get_messages(chat_id: str):
    messages = agents.get(chat_id)
    try:
        return Conversation(messages=messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No chat found with id {chat_id}")


@router.post("/chat", response_model=ChatMessage)
async def chat(message: ChatMessage):
    user = message.chat_user if message.chat_user else str(uuid.uuid4())
    query = message.message

    if agents.get(user):
        agent = agents.get(user)
        chats[user].extend([Message(sender="Cliente", message=query)])
    else:
        openai_config = OpenaiConfig(
            openai_key=configuration.openai_key,
            chat_model_version=configuration.chat_model_version,
        )
        qa = QaService(openai_config=openai_config)
        agent = qa.init_agent(tools=tools)
        agents[user] = agent
        chats[user] = [Message(sender="Cliente", message=query)]

    ## TODO save messages somewhere

    response = agent.invoke({"input": f"Cliente: {query}"})["output"]

    chats[user].extend([Message(sender="AI", message=response)])

    return ChatMessage(**{"sender": "AI", "message": response, "chat_user": user})
