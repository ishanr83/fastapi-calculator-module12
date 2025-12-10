from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root HTML endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "FastAPI Calculator" in response.text


def test_add_endpoint():
    """Test /api/add"""
    response = client.get("/api/add?a=5&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 8


def test_subtract_endpoint():
    """Test /api/subtract"""
    response = client.get("/api/subtract?a=10&b=4")
    assert response.status_code == 200
    assert response.json()["result"] == 6


def test_multiply_endpoint():
    """Test /api/multiply"""
    response = client.get("/api/multiply?a=6&b=7")
    assert response.status_code == 200
    assert response.json()["result"] == 42


def test_divide_endpoint():
    """Test /api/divide"""
    response = client.get("/api/divide?a=20&b=5")
    assert response.status_code == 200
    assert response.json()["result"] == 4


def test_divide_by_zero():
    """Test divide by zero error"""
    response = client.get("/api/divide?a=10&b=0")
    assert response.status_code == 400
    assert "detail" in response.json()
