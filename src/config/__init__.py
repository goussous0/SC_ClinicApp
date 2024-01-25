from os import environ
import redis.asyncio as redis
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, aliased
from api import api
from db import get_db
from auth import pass_hash
from models.user import User
from models.record import Record
from schema import UserType, Gender
from auth import TokenAuth
from db import engine
from fastapi_throttling import ThrottlingMiddleware

class App(FastAPI):
    def __init__(self):
        super().__init__()
        self.include_router(api)
        self.templates = Jinja2Templates(directory="templates")

        self.add_middleware(ThrottlingMiddleware,
                        limit=10,
                        window=60)

        User.metadata.create_all(bind=engine)
        Record.metadata.create_all(bind=engine)

        # add dummy data
        db = next(get_db())
        try:
            admin = User(username=environ['ADMIN_USERNAME'], passhash=pass_hash(environ['ADMIN_PASSWORD']), user_type=UserType.REGISTRAR, name="sysadmin") 

            doctor = User(username="anna", name="Anna", gender=Gender.FEMALE, phone="+940234112", passhash=pass_hash("123"), user_type=UserType.DOCTOR)
            patient = User(username="sara", name="Sara", gender=Gender.FEMALE, phone="+123423423", passhash=pass_hash("123"), user_type=UserType.PATIENT)
            db.add_all([admin, doctor, patient])
            db.commit()
        except IntegrityError:
            db.rollback()


        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["*"],
        )

        @self.get("/")
        async def home(request: Request):
            return self.templates.TemplateResponse("home.html", {"request": request})

        @self.get("/login")
        async def login(request: Request):
            return self.templates.TemplateResponse("login.html", {"request": request})

        @self.get("/patient")
        async def patient(request: Request, auth = Depends(TokenAuth())):
            return self.templates.TemplateResponse("patient.html", {"request": request, "user": auth.user})

        @self.get("/records")
        async def records(request: Request, auth = Depends(TokenAuth()), db: Session = Depends(get_db)):
            all_records = db.query(Record, User)
            if auth.user.user_type == UserType.DOCTOR:
                all_records = all_records.filter(Record.patient_id == User.id).all()
            elif auth.user.user_type == UserType.PATIENT:
                all_records = all_records.filter(Record.doctor_id == User.id).all()

            return self.templates.TemplateResponse("records.html", {"request": request, "user": auth.user, "records": all_records})

        @self.get("/patients")
        async def patients(request: Request, auth = Depends(TokenAuth()), db: Session = Depends(get_db)):
            all_patients = db.query(User).filter_by(user_type=UserType.PATIENT).all()
            return self.templates.TemplateResponse("patients.html", {"request": request, "user": auth.user, "patients": all_patients})

        @self.get("/doctors")
        async def doctors(request: Request, auth = Depends(TokenAuth())):
            all_doctors = db.query(User).filter_by(user_type=UserType.DOCTOR).all()
            return self.templates.TemplateResponse("doctors.html", {"request": request, "user": auth.user, "doctors": all_doctors})

        @self.get("/profile")
        async def profile(request: Request, auth = Depends(TokenAuth())):
            return self.templates.TemplateResponse("profile.html", {"request": request, "user": auth.user})

        @self.get("/logout")
        async def logout(request: Request):
            response = RedirectResponse(request.url_for('login'), 302)
            response.delete_cookie('token')
            return response
            