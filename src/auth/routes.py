from fastapi import APIRouter
from src.config import configuration

router = APIRouter()


@router.post("/user-create")
async def create_user():
    pass
