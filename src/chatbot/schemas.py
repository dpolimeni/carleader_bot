from pydantic import BaseModel, Field
from typing import List, Dict, Any


class Message(BaseModel):
    sender: str = Field(..., description="Who is sending the message")
    message: str = Field(..., description="Message content")


class ChatMessage(Message):
    chat_id: str = Field(None, description="identifier of the chat")
    extra: Any = Field(
        None, description="Extra parametri di messaggio ne caso venga ritornato un JSON"
    )


class Conversation(BaseModel):
    messages: List[Message]
