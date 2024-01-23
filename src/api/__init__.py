from os import environ
from sqlalchemy import union_all
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.logger import logger
from fastapi import (
    APIRouter,
    Depends,
    Request
)
from fastapi.responses import RedirectResponse
from fastapi_limiter.depends import RateLimiter

from db import get_db

from models.record import Record
from models.user import User

from schema import (
    LoginForm,
    NewRecord,
    UserType,
    NewUser,
    Gender,
)

from auth import verify_hash, create_access_token, pwd_context, TokenAuth


api = APIRouter(prefix="/api", dependencies=[Depends(RateLimiter(times=5, seconds=5))])

@api.post("/add_patient")
async def add_patient(request: Request, patient: NewUser = Depends(), db:Session = Depends(get_db), auth = Depends(TokenAuth())):
    try:
        new_patient = User(
            name=patient.name,
            age=patient.age,
            phone=patient.phone,
            gender=patient.gender,
            username=patient.username,
            passhash=pwd_context.hash(patient.password),
            user_type=UserType.PATIENT
        )
        db.add(new_patient)
        db.commit()
        return {"success": f"patient {new_patient.id} added"}
    except IntegrityError as e:
        logger.error(e)
        db.rollback()
        return {"error": "Failed to add patient"}
    
@api.post("/add_doctor")
async def add_doctor(request: Request, doctor: NewUser = Depends(), auth = Depends(TokenAuth()), db: Session = Depends(get_db)):
    try:
        new_doctor = User(
            name=doctor.name,
            age=doctor.age,
            phone=doctor.phone,
            gender=doctor.gender,
            username=doctor.username,
            passhash=pwd_context.hash(doctor.password),
            user_type=UserType.DOCTOR
        )
        db.add(new_doctor)
        db.commit()
        return {"success": f"doctor {new_doctor.id} added"}
    except IntegrityError as e:
        logger.error(e)
        db.rollback()
        return {"error": "Failed to add doctor"}


@api.post("/add_record")
async def add_record(request: Request, record: NewRecord = Depends(), db: Session = Depends(get_db), auth = Depends(TokenAuth())):
    try:
        new_record = Record(
            doctor_id = record.doctor_id,
            patient_id = record.patient_id,
            description = record.description,
            treatment = record.treatment,
        )
        db.add(new_record)
        db.commit()
        return {"success": f"record {new_record.id} added"}
    except IntegrityError as e:
        logger.error(e)
        db.rollback()
        return {"error": "Failed to add record"}

@api.post("/login")
async def post_login(request: Request, login_data: LoginForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=login_data.username).first()    
    if user and verify_hash(login_data.password, user.passhash):
        response = RedirectResponse(request.url_for("home"), 302)
        response.set_cookie(key="token", value=create_access_token(user))
        return response
    
    return RedirectResponse(request.url_for('logout'), 302)

