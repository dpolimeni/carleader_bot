from pydantic import BaseModel


class CarInfo(BaseModel):
    name: str
    id: str
    category: str  # Usato/Nuovo/chilometro 0
    traction: str
    power_type: str
    gearbox: str
    engine: str
    power: str  # kw/Cv
    mileage: str
    price: float
    type: str  # utilitaria/Berlina
    seats: int
    doors: int
    color_interior: str
    color_exterior: str
    warranty: str
    registration: str
    link: str
    image_link: str
    exposition: str


class OpenaiConfig(BaseModel):
    openai_key: str
    chat_model_version: str
    emb_model_version: str = None
