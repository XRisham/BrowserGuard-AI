from fastapi.testclient import TestClient
from app.main import app


def test_invalid_image_rejected() -> None:
    response = TestClient(app).post("/api/v1/classify/image", json={"image_base64": "not-valid-image"})
    assert response.status_code == 422
