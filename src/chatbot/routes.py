from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from src.chatbot.schemas import Message, Conversation, ChatMessage
from src.schemas import OpenaiConfig
from src.config import configuration
from src.chatbot.service import QaService
import uuid
import json

router = APIRouter()

chats = {}


@router.get("/chat", response_model=Conversation)
async def get_messages(chat_id: str):
    messages = chats.get(chat_id)
    try:
        print(messages)
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

    conversation = "\n".join([m.sender + ": " + m.message for m in chats.get(user, [])])

    prompt = f"""Ti verranno fornite la lista delle macchine disponibili in un concessionario. 
Il tuo compito è servire i clienti e proporgli le macchine più consone alle loro esigenze.
Quando proponi una macchina al cliente descrivigli alcune caratteristiche ed allega sempre il link dell'auto.

Questa è la conversazione con il cliente:
{conversation}
    
Questa è la lista delle macchine:
{formatted_json}
    """
    response = await qa.basic_answer(query, prompt)
    if chats.get(user):
        chats[user].extend(
            [
                Message(sender="Cliente", message=query),
                Message(sender="AI", message=response),
            ]
        )
    else:
        chats[user] = [
            Message(sender="Cliente", message=query),
            Message(sender="AI", message=response),
        ]

    agent = qa.init_agent()

    agent.invoke(
        {
            "input": f"Questa è la lista delle macchine:\n{formatted_json}. Questa è la richiesta del cliente: {query}"
        }
    )
    return ChatMessage(**{"sender": "AI", "message": response, "chat_user": user})
