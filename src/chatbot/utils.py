## HERE BUILD UTILS FUNCTION FOR THE SERVICE
from typing import Dict, List, Any
from langchain.agents import Tool
import json
from langchain.vectorstores import FAISS
from langchain.schema import SystemMessage
from langchain.embeddings.openai import OpenAIEmbeddings
from src.config import configuration


def jsonify_cars(chat_llm, num_iters: int, cars_proposal: str):
    prompt = f"""Il tuo compito e formattare la lista di macchine che ti viene fornita in formato JSON.
    Ritorna in output solamente il JSON.
    
    Il JSON deve contenere le caratteristiche di ogni macchina.
    Un esempio di JSON:
    
    {{
        "macchine": [
            {{
                "marca": "DACIA",
                "CV": "90",
                ...
            }},
            {{
                "marca": "FORD",
                "CV": "50",
                ...
            }}
        ],
    }}
    
    Ritorna in output solamente il JSON!!
    
    La lista di macchine è la seguente:
    {cars_proposal}
    """
    response = chat_llm([SystemMessage(content=prompt)])
    for _ in range(num_iters):
        try:
            print("TRY", _)
            result = json.loads(response.content)
        except Exception as e:
            prompt += f"Durante il parsing del JSON in output ho avuto questo errore: {e}. Ricorda di ritornare l'output in formato JSON!!"
            response = chat_llm([SystemMessage(content=prompt)])

    return result


def retrieve_cars(chat_llm, num_iters: int, query: str):
    embeddings = OpenAIEmbeddings(api_key=configuration.openai_key)
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(query)
    relevant_cars = "\n".join([d.page_content for d in docs])

    formatted_result = jsonify_cars(
        chat_llm=chat_llm, num_iters=num_iters, cars_proposal=relevant_cars
    )
    return str(formatted_result)


def init_tools(chat_llm):
    tools = [
        Tool.from_function(
            func=lambda cars_list: retrieve_cars(chat_llm, 3, cars_list),
            description="Usa questo tool per sapere le informazioni delle auto più adatte alla richiesta del cliente. In input prende una stringa che descrive le caratteristiche che cerchi in un'auto.",
            name="retrieve_cars",
            return_direct=True,
        ),
        # Tool.from_function(
        #    func=lambda cars_list: jsonify_cars(chat_llm, 3, cars_list),
        #    name="jsonify_cars",
        #    description="Tool per portare la proposta di macchine in formato JSON. Usa in input tutte le informazioni delle macchine (Nome, cavalli, link, posti etc..).",
        #    return_direct=True,
        # ),
    ]
    return tools
