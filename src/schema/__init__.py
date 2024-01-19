from pydantic import BaseModel
from fastapi import Form
from dataclasses import dataclass
from enum import Enum

class UserType(Enum):
    DOCTOR = "DOCTOR"
    PATIENT = "PATIENT"
    REGISTRAR = "REGISTRAR"

class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

@dataclass
class LoginForm:
    username: str = Form(...)
    password: str = Form(...)


@dataclass
class NewUser:
    name: str  = Form(...)
    age: int  = Form(...)
    gender: Gender = Form(...)
    phone: str = Form(...)
    username: str = Form(...)
    password: str = Form(...)

    # def __post_init__(self):
    #     self.phone = (self.phone.replace('+', '')
    #                         .replace('-', '')
    #                         .replace('(', '')
    #                         .replace(')', '')
    #     )
    #     print ("sanitize inputs")


@dataclass
class NewRecord:
    doctor_id: int = Form(...)
    patient_id: int = Form(...)
    description: str = Form(...)
    treatment: str = Form(...)