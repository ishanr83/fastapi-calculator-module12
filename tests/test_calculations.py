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


def create_user():
    response = client.post(
        "/users/register",
        json={
            "email": "calcuser@example.com",
            "username": "calcuser",
            "password": "secret123",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_calculation_bread():
    clear_db()
    user_id = create_user()

    response = client.post(
        "/calculations",
        json={
            "operation": "add",
            "operand_a": 2,
            "operand_b": 3,
            "user_id": user_id,
        },
    )
    assert response.status_code == 201
    calc = response.json()
    assert calc["result"] == 5
    calc_id = calc["id"]

    response = client.get("/calculations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    response = client.get(f"/calculations/{calc_id}")
    assert response.status_code == 200
    read_calc = response.json()
    assert read_calc["id"] == calc_id

    response = client.put(
        f"/calculations/{calc_id}",
        json={
            "operation": "multiply",
            "operand_a": 3,
            "operand_b": 4,
        },
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["result"] == 12

    response = client.delete(f"/calculations/{calc_id}")
    assert response.status_code == 204

    response = client.get(f"/calculations/{calc_id}")
    assert response.status_code == 404


def test_calculation_invalid_data():
    clear_db()
    user_id = create_user()

    response = client.post(
        "/calculations",
        json={
            "operation": "divide",
            "operand_a": 10,
            "operand_b": 0,
            "user_id": user_id,
        },
    )
    assert response.status_code == 400
