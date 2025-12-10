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
    """Test Browse, Read, Edit, Add, Delete"""
    clear_db()
    user_id = create_user()

    # Add - Create calculation
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

    # Browse - List all calculations
    response = client.get("/calculations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    # Read - Get single calculation
    response = client.get(f"/calculations/{calc_id}")
    assert response.status_code == 200
    read_calc = response.json()
    assert read_calc["id"] == calc_id

    # Edit - Update calculation
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

    # Delete
    response = client.delete(f"/calculations/{calc_id}")
    assert response.status_code == 204

    # Verify deletion
    response = client.get(f"/calculations/{calc_id}")
    assert response.status_code == 404


def test_calculation_invalid_data():
    """Test divide by zero"""
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


def test_all_operations():
    """Test all calculator operations"""
    clear_db()
    user_id = create_user()

    # Test add
    response = client.post(
        "/calculations",
        json={"operation": "add", "operand_a": 5, "operand_b": 3, "user_id": user_id},
    )
    assert response.status_code == 201
    assert response.json()["result"] == 8

    # Test subtract
    response = client.post(
        "/calculations",
        json={"operation": "subtract", "operand_a": 10, "operand_b": 4, "user_id": user_id},
    )
    assert response.status_code == 201
    assert response.json()["result"] == 6

    # Test multiply
    response = client.post(
        "/calculations",
        json={"operation": "multiply", "operand_a": 6, "operand_b": 7, "user_id": user_id},
    )
    assert response.status_code == 201
    assert response.json()["result"] == 42

    # Test divide
    response = client.post(
        "/calculations",
        json={"operation": "divide", "operand_a": 20, "operand_b": 5, "user_id": user_id},
    )
    assert response.status_code == 201
    assert response.json()["result"] == 4


def test_invalid_operation():
    """Test invalid operation"""
    clear_db()
    user_id = create_user()

    response = client.post(
        "/calculations",
        json={"operation": "modulo", "operand_a": 10, "operand_b": 3, "user_id": user_id},
    )
    assert response.status_code == 400


def test_invalid_user():
    """Test calculation with non-existent user"""
    clear_db()

    response = client.post(
        "/calculations",
        json={"operation": "add", "operand_a": 5, "operand_b": 3, "user_id": 9999},
    )
    assert response.status_code == 400


def test_update_nonexistent_calculation():
    """Test updating non-existent calculation"""
    clear_db()

    response = client.put(
        "/calculations/9999",
        json={"operation": "add", "operand_a": 1, "operand_b": 2},
    )
    assert response.status_code == 404


def test_delete_nonexistent_calculation():
    """Test deleting non-existent calculation"""
    clear_db()

    response = client.delete("/calculations/9999")
    assert response.status_code == 404


def test_update_with_invalid_operation():
    """Test update with invalid operation"""
    clear_db()
    user_id = create_user()

    # Create a calculation
    response = client.post(
        "/calculations",
        json={"operation": "add", "operand_a": 2, "operand_b": 3, "user_id": user_id},
    )
    calc_id = response.json()["id"]

    # Try to update with invalid operation
    response = client.put(
        f"/calculations/{calc_id}",
        json={"operation": "invalid"},
    )
    assert response.status_code == 400


def test_partial_update():
    """Test partial update of calculation"""
    clear_db()
    user_id = create_user()

    # Create a calculation
    response = client.post(
        "/calculations",
        json={"operation": "add", "operand_a": 5, "operand_b": 3, "user_id": user_id},
    )
    calc_id = response.json()["id"]

    # Update only operand_a
    response = client.put(
        f"/calculations/{calc_id}",
        json={"operand_a": 10},
    )
    assert response.status_code == 200
    assert response.json()["result"] == 13

    # Update only operand_b
    response = client.put(
        f"/calculations/{calc_id}",
        json={"operand_b": 7},
    )
    assert response.status_code == 200
    assert response.json()["result"] == 17
