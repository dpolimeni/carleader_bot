from abc import ABC
from typing import Dict


# Abstract class for q&a
class BaseQA(ABC):
    async def basic_retrieval(self, query: str) -> Dict[str, str]:
        pass

    async def basic_answer(self, query: str, context: str) -> str:
        pass

    ## TODO if we need them add params
    async def basic_qa_agent(self):
        pass

    ## TODO implement different types of Q&A agent init
