from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from src.config import configuration
from src.database import make_session
from src.auth.models import User
from src.auth.schemas import UserCreate


router = APIRouter()


@router.post("/user-create")
async def create_user(db: Annotated[Session, Depends(make_session)], user: UserCreate):
    new_user = User(
        username=user.username,
        hashed_password=user.password,
        email=user.email,
    )
    db.add(new_user)

    # Commit the transaction
    db.commit()

    # Close the session
    db.close()
    return {"response": "user created"}
