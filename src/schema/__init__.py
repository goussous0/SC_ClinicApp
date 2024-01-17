from pydantic import BaseModel
from fastapi import Form
from dataclasses import dataclass
from enum import Enum

class UserType(Enum):
    DOCTOR = "DOCTOR"
    PATIENT = "PATIENT"


@dataclass
class LoginForm:
    username: str = Form(...)
    password: str = Form(...)