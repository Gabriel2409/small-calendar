from fastapi.testclient import TestClient


def test_hello(test_app: TestClient):
    """Tests of the hello route to ensure the app is working as intended"""
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World", "env": "testing"}
