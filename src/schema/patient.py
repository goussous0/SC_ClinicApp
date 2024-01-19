from schema import Gender
from dataclasses import dataclass
from fastapi import Form


@dataclass
class NewPatient:
    name: str  = Form(...)
    age: int  = Form(...)
    gender: Gender = Form(...)
    phone: str = Form(...)
    username: str = Form(...)
    password: str = Form(...)