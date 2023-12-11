from src.database import Base
from sqlalchemy import Column, Integer, String
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String)
    hashed_password = Column(String)

    @property
    def password(self):
        return "Cannot get the password"

    @password.setter
    def password(self, new_password):
        self.hashed_password = pwd_context.hash(new_password)

    def check_password(self, password):
        print("NEL MODELLO")
        print(pwd_context.verify(password, self.hashed_password))
        return pwd_context.verify(password, self.hashed_password)
