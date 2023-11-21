## HERE BUILD UTILS FUNCTION FOR THE SERVICE
from typing import Dict, List, Any
from langchain.agents import Tool
import json
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from src.config import configuration


def format_cars(cars_dict: List[Dict[str, str]]) -> str:
    explanation = """La lista di macchine che ti verrnno fornite hanno queste specifiche: 
    name: nome dell'auto
    category: categoria se usato o nuovo
    traction: tipo di trazione (anteriore posteriore 4x4)
    power_type: il tipo di alimentazione (Gas, DIesel o benzina)
    gearbox: Il cambio se automatico o manuale
    engine: Cilindrata del motore
    power: potenza del motore Kilowatt (Cavalli)
    mileage: Chilometri percorsi
    price: Prezzo in euro
    type: Tipo di macchina (Utilitaria/Berlina)
    seats: Numero di posti
    doors: Numero di porte
    color_interior: Colori interni
    color_exterior: Colori esterni
    warranty: Garaniza dell'auto
    registration: data di immatricolazione 
    link: link all'auto online
    """


def retrieve_cars(query: str):
    with open("src/cars.json", "r") as f:
        cars = json.load(f)
    embeddings = OpenAIEmbeddings(api_key=configuration.openai_key)
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(query)
    relevant_cars = "\n".join([d.page_content for d in docs])
    formatted_json = json.dumps(cars, indent=2)
    return relevant_cars


def init_tools():
    tools = [
        Tool.from_function(
            func=retrieve_cars,
            description="Usa questo tool per conoscere le macchine disponibili nel concessionario. In input prende una stringa che descrive le caratteristiche che cerchi in un'auto.",
            name="retrieve_cars",
        )
    ]
    return tools
