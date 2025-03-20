# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_all_campaigns():
    response = client.get("/campaigns/?start_date=2023-01-01&end_date=2023-12-31")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
