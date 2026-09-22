from fastapi.testclient import TestClient
from app.main import app


def test_blocklist_overrides_model() -> None:
    response = TestClient(app).post("/api/v1/classify/page", json={"url": "https://bad.example", "text": "plain", "blocklist": ["bad.example"]})
    assert response.status_code == 200
    assert response.json()["decision"] == "BLOCK"
