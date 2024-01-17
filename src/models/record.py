from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base

class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("users.id"))
    patient_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String)
    treatment = Column(String)
