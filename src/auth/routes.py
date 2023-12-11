from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from typing import Annotated, Any
from src.database import make_session
from src.auth.models import User
from src.auth.schemas import UserCreate, UserLogin
from src.auth.utils import create_access_token  # get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


router = APIRouter()


def get_user(db: Session, username):
    query = select(User).where(User.username == username)
    query_result = db.scalars(query)
    user = query_result.first()
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(make_session)],
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/user-create")
async def create_user(db: Annotated[Session, Depends(make_session)], user: UserCreate):
    new_user = User(
        username=user.username,
        password=user.password,
        email=user.email,
    )
    db.add(new_user)

    # Commit the transaction
    db.commit()

    # Close the session
    db.close()
    return {"response": "user created"}


##user_data: UserLogin
@router.post("/login")
async def login(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(make_session)],
):
    query = select(User).where(User.username == user_data.username)
    query_result = db.scalars(query)
    user = query_result.first()

    password_chek = user.check_password(user_data.password) if user else False
    print("PASSWORD", password_chek)
    if not (user and password_chek):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=1)
    access_token = create_access_token(
        data={"sub": user.username, "email": user.email},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/all")
async def get_users(
    db: Annotated[Session, Depends(make_session)],
    current_user: Annotated[Any, Depends(get_current_user)],
):
    query = select(User)
    query_result = db.scalars(query)
    result = query_result.unique().all()
    return result
