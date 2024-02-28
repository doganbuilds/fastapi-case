from fastapi.testclient import TestClient
from app.main import app
from app.model import Post

client = TestClient(app)


def test_home_without_data():
    response = client.get("/posts")
    assert response.status_code == 200
    assert response.json() == []
