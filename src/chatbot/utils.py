## HERE BUILD UTILS FUNCTION FOR THE SERVICE
from typing import Dict, List, Union, Any
import json
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from openai import OpenAI
from src.config import configuration


def retrieve_cars(query: str, openai_client: OpenAI) -> Dict[str, Union[str, dict]]:
    """Retrieve cars relevant for the user query and return them alongside a text proposition"""
    embeddings = OpenAIEmbeddings(api_key=configuration.openai_key)
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(query)
    relevant_cars = [d.metadata for d in docs]
    relevant_cars_text = "\n".join([d.page_content for d in docs])

    response = openai_client.chat.completions.create(
        model=configuration.chat_model_version,
        messages=[
            {
                "role": "system",
                "content": f"""Devi proporre le seguenti macchine: {relevant_cars_text}. Quando ti rivolgi al cliente spiegagli perche queste macchine sono adatte alle sue esigenze. 
Il cliente che ha chiesto queste specifiche: {query}.""",
            },
        ],
    )
    response_message = response.choices[0].message.content

    response = {"message": response_message, "extra": relevant_cars}
    return response


def init_client_tools() -> List[Dict[str, Any]]:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "retrieve_cars",
                "description": "Usa questo tool per sapere le informazioni delle auto più adatte alla richiesta del cliente. In input prende una stringa che descrive le caratteristiche che cerchi in un'auto.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Le caratteristiche dell'auto che cerca il cliente",
                        },
                    },
                    "required": ["query"],
                },
            },
        }
    ]
    return tools


def execute_client_tools(message, openai_client) -> Dict[str, Union[str, dict]]:
    """Execute tools decided by the openai client."""
    if message.tool_calls[0].function.name == "retrieve_cars":
        query = json.loads(message.tool_calls[0].function.arguments)["query"]
        results = retrieve_cars(query, openai_client)
    else:
        results = f"Error: function {message['tool_calls'][0]['function']['name']} does not exist"
    return results


# DO not use langchain agents until Azure OpenAI
# def retrieve_cars(chat_llm, num_iters: int, query: str):
#     embeddings = OpenAIEmbeddings(api_key=configuration.openai_key)
#     print("CREATING DB")
#     new_db = FAISS.load_local("faiss_index", embeddings)
#     print("QUERYING")
#     docs = new_db.similarity_search(query)
#     print("DONE")
#     relevant_cars = "\n".join([d.page_content for d in docs])
#     print(relevant_cars[:100])
#     formatted_result = jsonify_cars(
#         chat_llm=chat_llm, num_iters=num_iters, cars_proposal=relevant_cars
#     )
#     return str(formatted_result)

# def init_tools(chat_llm):
#     tools = [
#         Tool.from_function(
#             func=lambda cars_list: retrieve_cars(chat_llm, 3, cars_list),
#             description="Usa questo tool per sapere le informazioni delle auto più adatte alla richiesta del cliente. In input prende una stringa che descrive le caratteristiche che cerchi in un'auto.",
#             name="retrieve_cars",
#             return_direct=True,
#         ),
#         # Tool.from_function(
#         #    func=lambda cars_list: jsonify_cars(chat_llm, 3, cars_list),
#         #    name="jsonify_cars",
#         #    description="Tool per portare la proposta di macchine in formato JSON. Usa in input tutte le informazioni delle macchine (Nome, cavalli, link, posti etc..).",
#         #    return_direct=True,
#         # ),
#     ]
#     return tools
