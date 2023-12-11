from datetime import timedelta, datetime
from jose import JWTError, jwt
from fastapi.exceptions import HTTPException
from fastapi import Depends
from typing import Annotated


def create_access_token(data, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "SECRET_KEY", algorithm="HS256")
    return encoded_jwt
