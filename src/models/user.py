from sqlalchemy import Integer, Column, String, Enum
from db import Base
from schema import UserType, Gender

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    name = Column(String)
    phone = Column(String)
    gender = Column(Enum(Gender), default=None)
    passhash = Column(String)
    username = Column(String, unique=True)
    user_type = Column(Enum(UserType))
