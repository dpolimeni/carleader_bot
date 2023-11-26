from fastapi import APIRouter
import uuid
import json
from fastapi.exceptions import HTTPException
from src.chatbot.schemas import Conversation, ChatMessage, Message
from src.schemas import OpenaiConfig
from src.config import configuration
from src.chatbot.service import QaService
from src.chatbot.utils import init_tools
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI

router = APIRouter()

agents = {}
chats = {}
chat_llm = ChatOpenAI(
    temperature=0,
    openai_api_key=configuration.openai_key,
    model=configuration.chat_model_version,
    request_timeout=15,
)
tools = init_tools(chat_llm)


@router.get("/chat", response_model=Conversation)
async def get_messages(chat_id: str):
    messages = chats.get(chat_id)
    try:
        return Conversation(messages=messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No chat found with id {chat_id}")


@router.post("/chat", response_model=ChatMessage)
async def chat(message: ChatMessage):
    user = message.chat_id if message.chat_id else str(uuid.uuid4())
    query = message.message

    openai_config = OpenaiConfig(
        openai_key=configuration.openai_key,
        chat_model_version=configuration.chat_model_version,
    )
    qa = QaService(openai_config=openai_config)

    if agents.get(user):
        agent = agents.get(user)
        chats[user].extend([Message(sender="Cliente", message=query)])
    else:
        agent = qa.init_agent(tools=tools)
        agents[user] = agent
        chats[user] = [Message(sender="Cliente", message=query)]

    ## TODO save messages somewhere

    response = agent.invoke({"input": f"Cliente: {query}"})  # ["output"].strip()
    # relevant_cars = "\n".join([d.page_content for d in docs])

    # prompt = f"""Ti verranno fornite la lista delle macchine disponibili in un concessionario.
    # Il tuo compito è servire i clienti e proporgli le macchine più consone alle loro esigenze.
    # Quando proponi una macchina al cliente descrivigli alcune caratteristiche ed allega sempre il link dell'auto.
    #
    # Questa è la conversazione con il cliente:
    # {conversation}
    #
    # Questa è la lista delle macchine:
    # {relevant_cars}
    #    """
    # response = await qa.basic_answer(query, context=prompt)
    # description = await qa.basic_answer(
    #    query="Fai una descrizione delle macchine presenti e proponile ad un cliente",
    #    context=str(response["output"]),
    # )
    chats[user].extend([Message(sender="AI", message=str(response["output"]))])

    return ChatMessage(
        **{
            "sender": "AI",
            "message": response["output"],
            "chat_id": user,
            "extra": response["output"],
        }
    )
