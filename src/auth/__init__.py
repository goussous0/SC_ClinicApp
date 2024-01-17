from typing import List
from jose import jwt
from fastapi import HTTPException, Depends, Request, status
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose.exceptions import ExpiredSignatureError
from random import choice, sample
from string import digits, ascii_letters
from schema import UserType
from models.user import User
from db import get_db
from sqlalchemy.orm import Session

SECRET_KEY = ''.join(sample(list(digits+ascii_letters), 32))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(user: User):
    now = datetime.now()
    expire = now + timedelta(hours=4)    # token valid for 4 hours
    to_encode = {"exp": expire.timestamp(), "username": user.username, "usertype": user.user_type.value}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256") 
    return encoded_jwt

def verify_token(token, user):
    token = request.cookies.get("token")
    if token:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_type = payload["usertype"].upper()
        username = payload["username"]

    
    raise HTTPException(status_code=401, headers={"Location": "/logout"})

def verify_hash(password, passhash):
        return pwd_context.verify(password, passhash)

def pass_hash(password):
    return pwd_context.hash(password)


class TokenAuth:
    def __call__(self, request: Request, db: Session = Depends(get_db)):
        self.user = None
        token = request.cookies.get("token")
        if token:
            try:

                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            except ExpiredSignatureError:
                raise HTTPException(status_code=401, headers={"Location": "/logout"})

            try:
                user = db.query(User).filter_by(username=data["username"]).first()
                if user:
                    self.user = user
            except KeyError:
                raise HTTPException(status_code=401, headers={"Location": "/logout"})

        return self

