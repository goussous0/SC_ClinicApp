from sqlalchemy import union_all
from sqlalchemy.orm import Session
from fastapi import (
    APIRouter,
    Depends,
    Request
)
from fastapi.responses import RedirectResponse

from db import get_db

from models.record import Record
from models.user import User

from schema import LoginForm

from auth import verify_hash, create_access_token


api = APIRouter(prefix="/api")

@api.post("/add_patient")
async def add_patient(request: Request):
    return {"hello": "world"}
    
@api.post("/add_doctor")
async def add_doctor(request: Request):
    return {"hello": "world"}

@api.post("/add_record")
async def add_record(request: Request):
    return {"hello": "world"}

@api.post("/login")
async def post_login(request: Request, login_data: LoginForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=login_data.username).first()    
    if user and verify_hash(login_data.password, user.passhash):
        response = RedirectResponse(request.url_for("home"), 302)
        response.set_cookie(key="token", value=create_access_token(user))
        return response
    
    return RedirectResponse(request.url_for('logout'), 302)

