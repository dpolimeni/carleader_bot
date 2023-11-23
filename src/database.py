from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from collections.abc import Generator


engine = create_engine("sqlite://", echo=True)


class Base(DeclarativeBase):
    pass


def make_session() -> Generator[Session, None]:
    with Session(engine) as session:
        yield session
