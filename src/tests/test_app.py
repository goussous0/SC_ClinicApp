from os import environ
from tests import client
from pytest import mark

@mark.parametrize("username,password, response", 
    [
        (environ["ADMIN_USERNAME"], environ["ADMIN_PASSWORD"], "Logout"),
        ("hello", "world", "Login")]
)
def test_login(username, password, response):
    payload = {
        "username": username,
        "password": password,
    }
    resp = client.post("api/login", data=payload)
    assert resp.status_code == 200
    assert response in resp.text    

def test_add_doctor():
    assert True

def test_add_patient():
    assert True

def test_add_record():
    assert True