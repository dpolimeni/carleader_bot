from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from src.config import configuration
from src.database import make_session
from src.auth.models import User


router = APIRouter()


@router.get("/user-create")
async def create_user(db: Annotated[Session, Depends(make_session)]):
    print(db.query(User).all())
    return {"test": "test"}
