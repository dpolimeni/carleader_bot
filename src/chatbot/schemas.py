from pydantic import BaseModel, Field
from typing import List


class Message(BaseModel):
    sender: str = Field(..., description="Who is sending the message")
    message: str = Field(..., description="Message content")


class ChatMessage(Message):
    chat_user: str = Field(None, description="identifier of the chat")


class Conversation(BaseModel):
    messages: List[Message]
