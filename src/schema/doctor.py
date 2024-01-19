from schema import Gender
from fastapi import Form
from dataclasses import dataclass

@dataclass
class NewDoctor:
    name: str  = Form(...)
    age: int  = Form(...)
    gender: Gender = Form(...)
    phone: str = Form(...)
    username: str = Form(...)
    password: str = Form(...)