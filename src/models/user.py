from sqlalchemy import Integer, Column, String, Enum
from db import Base
from schema import UserType

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    name = Column(String, unique=True)
    phone = Column(String)
    gender = Column(String)
    passhash = Column(String)
    username = Column(String, unique=True)
    user_type = Column(Enum(UserType))
