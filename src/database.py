from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from collections.abc import Generator
import os


engine = create_engine("sqlite:///example.db", echo=True)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def make_session() -> Generator[Session, None]:
    with Session(engine) as session:
        yield session
