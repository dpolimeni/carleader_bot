from fastapi import APIRouter
from chatbot.schemas import Message, Conversation

router = APIRouter()


@router.get("/chat", response_model=Conversation)
def get_messages():
    return Conversation(
        **{"messages": [Message(**{"sender": "test", "message": "test"})]}
    )


@router.post("/chat", response_model=Message)
def read_user(message: Message):
    return {"sender": "test", "message": "test"}
