from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import SystemMessage, HumanMessage
from src.chatbot.service_abc import BaseQA
from src.schemas import OpenaiConfig
from typing import List, Any

## TODO check if we need a retriever


class QaService(BaseQA):
    def __init__(
        self, openai_config: OpenaiConfig, local_models: List[Any] = None
    ) -> None:
        """Init is done with the openai key and local models (whatever they are)"""

        self.chat_llm = ChatOpenAI(
            temperature=0,
            openai_api_key=openai_config.openai_key,
            model=openai_config.chat_model_version,
            request_timeout=15,
        )

        self.emb_llm = OpenAIEmbeddings(
            openai_api_key=openai_config.openai_key, client=None
        )

    async def basic_answer(self, query: str, context: str) -> str:
        messages = [SystemMessage(content=context), HumanMessage(content=query)]

        response = self.chat_llm(messages)

        return response.content
