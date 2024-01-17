from sqlalchemy import Column, Integer, String
from db import Base

class Registrar(Base):
    __tablename__ = "registrar"
    id = Column(Integer, primary_key=True, index=True)
    passhash = Column(String)
    username = Column(String, unique=True)
