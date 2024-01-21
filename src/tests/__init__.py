import os
from config import App
from fastapi.testclient import TestClient

app = App()
client  = TestClient(app)

