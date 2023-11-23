from fastapi import APIRouter, Depends
from src.config import configuration
from src.database import make_session


router = APIRouter()


@router.post("/user-create")
async def create_user(db: Depends(make_session)):
    pass
