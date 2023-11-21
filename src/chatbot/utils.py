## HERE BUILD UTILS FUNCTION FOR THE SERVICE
from typing import Dict, List, Any
from langchain.agents import Tool
import json


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


def retrieve_cars(placeholder: Any):
    with open("src/cars.json", "r") as f:
        cars = json.load(f)

    formatted_json = json.dumps(cars, indent=2)
    return formatted_json


def init_tools():
    tools = [
        Tool.from_function(
            func=retrieve_cars,
            description="Usa questo tool per conoscere le macchine disponibili nel concessionario",
            name="retrieve_cars",
        )
    ]
    return tools
