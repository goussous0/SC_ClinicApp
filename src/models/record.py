from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db import Base

class Record(Base):
    __tablename__ = "records"
    __table_args__ = (UniqueConstraint("doctor_id", "patient_id"),)
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("users.id"))
    patient_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String)
    treatment = Column(String)
    

