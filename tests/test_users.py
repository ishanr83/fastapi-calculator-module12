from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app import models

client = TestClient(app)


def setup_module():
    Base.metadata.create_all(bind=engine)


def teardown_module():
    Base.metadata.drop_all(bind=engine)


def clear_db():
    db = SessionLocal()
    db.query(models.Calculation).delete()
    db.query(models.User).delete()
    db.commit()
    db.close()


def test_user_register_and_login():
    clear_db()

    response = client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "secret123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    user_id = data["id"]

    response = client.post(
        "/users/login",
        json={
            "email": "test@example.com",
            "password": "secret123",
        },
    )
    assert response.status_code == 200
    login_data = response.json()
    assert login_data["id"] == user_id
    assert login_data["email"] == "test@example.com"


def test_login_invalid_password():
    clear_db()

    response = client.post(
        "/users/register",
        json={
            "email": "badpass@example.com",
            "username": "baduser",
            "password": "goodpass",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/users/login",
        json={
            "email": "badpass@example.com",
            "password": "wrongpass",
        },
    )
    assert response.status_code == 401
