from os import environ
from pytest import fixture

environ["DB_URI"] = "sqlite:///test_records.db"

@fixture
def test_db_session():
    # Use an SQLite in-memory database for testing
    engine = create_engine(environ["DB_URI"])
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

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