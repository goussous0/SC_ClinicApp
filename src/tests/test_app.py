from os import environ
from pytest import mark
from re import match, compile
from db import get_db
from tests import client, admin_user, delay

@mark.parametrize("username,password, token, response",  
    [
        (environ["ADMIN_USERNAME"], environ["ADMIN_PASSWORD"], True, "Logout"),
        ("hello", "world", False, "Login")
    ]
)
def test_login(username, password, token, response, delay):
    payload = {
        "username": username,
        "password": password,
    }
    resp = client.post("api/login", data=payload, allow_redirects=False)
    assert resp.status_code == 302
    assert bool(resp.cookies.get("token")) == token 


# possible values to be inserted in the form fields 
@mark.parametrize("age, name, phone, gender, password, username, user_type, msg_type, msg_value" ,
    [
        # DOCTOR 
        (32, "Mike", "+962-6-5863195", "MALE", "s0_s3cur3", "mike", "doctor", "success", r"doctor \d added"),
        (32, "Mike", "+962-6-5863195", "MALE", "s0_s3cur3", "mike", "doctor", "error", r"Failed to add doctor"),        

        # PATIENT 
        (32, "Lera", "+945-5-8092348", "FEMALE", "l3t_m3_1n", "lera", "patient", "success", r"patient \d added"),
        (32, "Lera", "+945-5-8092348", "FEMALE", "l3t_m3_1n", "lera", "patient", "error", r"Failed to add patient"),    
    ]
)
def test_add_user(age, name, phone, gender, password, username, user_type, msg_type, msg_value, admin_user, delay):
    payload = {
        "age": age,
        "name": name,
        "phone": phone,
        "gender": gender,
        "password": password,
        "username": username
    }
    resp = client.post(f"api/add_{user_type}", data=payload, cookies=admin_user.cookies)
    
    assert resp.status_code == 200 
    assert bool(match(msg_value, resp.json()[msg_type])) 


@mark.parametrize("patient_id, doctor_id, description, treatment, msg_type, msg_value",
    [
        (3, 2, "headache, high temperature", "aspirin", "success", r"record \d added"),
        (3, 2, "stomach ache", "Pepto-Bismol", "error", r"Failed to add record")
    ]
)
def test_add_record(patient_id, doctor_id, description, treatment, msg_type, msg_value, admin_user, delay):
    payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "description": description,
        "treatment": treatment
    }
    resp = client.post(f"api/add_record", data=payload, cookies=admin_user.cookies)
    
    assert resp.status_code == 200 
    assert bool(match(msg_value, resp.json()[msg_type])) 



def test_database_connection():
    db = next(get_db())
    assert db.connection().closed == 0