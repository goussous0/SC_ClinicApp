from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError
from api import api
from db import get_db
from auth import pass_hash
from models.user import User
from models.registrar import Registrar
from models.record import Record
from schema import UserType
from auth import TokenAuth
from db import engine

class App(FastAPI):
    def __init__(self):
        super().__init__()
        self.include_router(api)
        self.templates = Jinja2Templates(directory="templates")
        

        User.metadata.create_all(bind=engine)
        Registrar.metadata.create_all(bind=engine)
        Record.metadata.create_all(bind=engine)

        # add dummy data 
        db = next(get_db())
        try:
            admin = Registrar(username="admin", passhash=pass_hash("123")) 

            doctor = User(username="anna", name="Anna", gender="female", phone="+940234112", passhash=pass_hash("123"), user_type=UserType.DOCTOR)
            patient = User(username="sara", name="Sara", gender="female", phone="+12342342", passhash=pass_hash("123"), user_type=UserType.PATIENT)
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
        async def home(request: Request, auth = Depends(TokenAuth())):
            return self.templates.TemplateResponse("home.html", {"request": request, "user": auth.user})

        @self.get("/login")
        async def login(request: Request):
            return self.templates.TemplateResponse("login.html", {"request": request})

        @self.get("/patient")
        async def patient(request: Request, auth = Depends(TokenAuth())):
            return self.templates.TemplateResponse("patient.html", {"request": request, "user": auth.user})

        @self.get("/records")
        async def records(request: Request, auth = Depends(TokenAuth())):
            return self.templates.TemplateResponse("records.html", {"request": request, "user": auth.user})

        @self.get("/patients")
        async def patients(request: Request, auth = Depends(TokenAuth())):
            return self.templates.TemplateResponse("patients.html", {"request": request, "user": auth.user})

        @self.get("/profile")
        async def profile(request: Request, auth = Depends(TokenAuth())):
            return self.templates.TemplateResponse("profile.html", {"request": request, "user": auth.user})

        @self.get("/logout")
        async def logout(request: Request):
            response = RedirectResponse(request.url_for('login'), 302)
            response.delete_cookie('token')
            return response
