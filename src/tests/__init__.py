from os import environ
from time import sleep
from pytest import fixture

# sqlite for testing only 
environ["DB_URI"] = "sqlite:///test_records.db"
environ["ADMIN_USERNAME"] = "admin"
environ["ADMIN_PASSWORD"] = "123"

@fixture
def test_db_session():
    engine = create_engine(environ["DB_URI"])
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

@fixture
def delay():
    sleep(10)

@fixture
def admin_user():
    payload = {
        "username": environ["ADMIN_USERNAME"],
        "password": environ["ADMIN_PASSWORD"]
    }
    resp = client.post("api/login", data=payload, allow_redirects=False)
    return resp

from config import App
from fastapi.testclient import TestClient

app = App()
client  = TestClient(app)