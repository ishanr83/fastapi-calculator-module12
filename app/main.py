from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List

import app.operations as op
from app import models, schemas, auth
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Calculator - Module 12")


@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI Calculator - Module 12</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 600px; 
            margin: 50px auto; 
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { 
            color: #333; 
            text-align: center;
        }
        input, select, button { 
            margin: 10px 5px; 
            padding: 12px; 
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #45a049;
        }
        #result { 
            margin-top: 20px; 
            padding: 15px; 
            background: #e8f5e9; 
            border-radius: 5px; 
            min-height: 20px;
            font-weight: bold;
            color: #2e7d32;
        }
        .error {
            background: #ffebee !important;
            color: #c62828 !important;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>FastAPI Calculator</h1>
        <p style="text-align: center; color: #666;">Module 12: Docker + PostgreSQL</p>
        <div>
            <input type="number" id="a" placeholder="First Number" step="any">
            <input type="number" id="b" placeholder="Second Number" step="any">
        </div>
        <div>
            <select id="operation">
                <option value="add">Add (+)</option>
                <option value="subtract">Subtract (-)</option>
                <option value="multiply">Multiply (×)</option>
                <option value="divide">Divide (÷)</option>
            </select>
            <button onclick="calculate()">Calculate</button>
        </div>
        <div id="result"></div>
    </div>
    <script>
        async function calculate() {
            const a = document.getElementById('a').value;
            const b = document.getElementById('b').value;
            const operation = document.getElementById('operation').value;
            const resultDiv = document.getElementById('result');
            
            if (!a || !b) {
                resultDiv.textContent = 'Please enter both numbers';
                resultDiv.className = 'error';
                return;
            }
            
            try {
                const response = await fetch(`/api/${operation}?a=${a}&b=${b}`);
                const data = await response.json();
                
                if (response.ok) {
                    resultDiv.textContent = `Result: ${data.result}`;
                    resultDiv.className = '';
                } else {
                    resultDiv.textContent = `Error: ${data.detail}`;
                    resultDiv.className = 'error';
                }
            } catch (error) {
                resultDiv.textContent = `Error: ${error.message}`;
                resultDiv.className = 'error';
            }
        }
    </script>
</body>
</html>
"""
    return html_content


def _calc(func, a: float, b: float) -> float:
    try:
        return func(a, b)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/add")
def add(a: float, b: float):
    return {"operation": "add", "result": _calc(op.add, a, b)}


@app.get("/api/subtract")
def subtract(a: float, b: float):
    return {"operation": "subtract", "result": _calc(op.subtract, a, b)}


@app.get("/api/multiply")
def multiply(a: float, b: float):
    return {"operation": "multiply", "result": _calc(op.multiply, a, b)}


@app.get("/api/divide")
def divide(a: float, b: float):
    return {"operation": "divide", "result": _calc(op.divide, a, b)}


@app.post("/users/register", response_model=schemas.UserRead, status_code=201)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_email = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_username = db.query(models.User).filter(models.User.username == user_in.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = auth.get_password_hash(user_in.password)
    user = models.User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/users/login", response_model=schemas.UserRead)
def login_user(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not auth.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return user


@app.get("/calculations", response_model=List[schemas.CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    calculations = db.query(models.Calculation).all()
    return calculations


@app.get("/calculations/{calculation_id}", response_model=schemas.CalculationRead)
def read_calculation(calculation_id: int, db: Session = Depends(get_db)):
    calculation = db.query(models.Calculation).filter(models.Calculation.id == calculation_id).first()
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calculation


@app.post("/calculations", response_model=schemas.CalculationRead, status_code=201)
def add_calculation(calc_in: schemas.CalculationCreate, db: Session = Depends(get_db)):
    if calc_in.operation not in {"add", "subtract", "multiply", "divide"}:
        raise HTTPException(status_code=400, detail="Invalid operation")

    user = db.query(models.User).filter(models.User.id == calc_in.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    try:
        if calc_in.operation == "add":
            result = op.add(calc_in.operand_a, calc_in.operand_b)
        elif calc_in.operation == "subtract":
            result = op.subtract(calc_in.operand_a, calc_in.operand_b)
        elif calc_in.operation == "multiply":
            result = op.multiply(calc_in.operand_a, calc_in.operand_b)
        else:
            result = op.divide(calc_in.operand_a, calc_in.operand_b)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    calculation = models.Calculation(
        operation=calc_in.operation,
        operand_a=calc_in.operand_a,
        operand_b=calc_in.operand_b,
        result=result,
        user_id=calc_in.user_id,
    )
    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    return calculation


@app.put("/calculations/{calculation_id}", response_model=schemas.CalculationRead)
def edit_calculation(
    calculation_id: int,
    calc_update: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
):
    calculation = db.query(models.Calculation).filter(models.Calculation.id == calculation_id).first()
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")

    if calc_update.operation is not None:
        if calc_update.operation not in {"add", "subtract", "multiply", "divide"}:
            raise HTTPException(status_code=400, detail="Invalid operation")
        calculation.operation = calc_update.operation

    if calc_update.operand_a is not None:
        calculation.operand_a = calc_update.operand_a
    if calc_update.operand_b is not None:
        calculation.operand_b = calc_update.operand_b

    try:
        if calculation.operation == "add":
            calculation.result = op.add(calculation.operand_a, calculation.operand_b)
        elif calculation.operation == "subtract":
            calculation.result = op.subtract(calculation.operand_a, calculation.operand_b)
        elif calculation.operation == "multiply":
            calculation.result = op.multiply(calculation.operand_a, calculation.operand_b)
        else:
            calculation.result = op.divide(calculation.operand_a, calculation.operand_b)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db.commit()
    db.refresh(calculation)
    return calculation


@app.delete("/calculations/{calculation_id}", status_code=204)
def delete_calculation(calculation_id: int, db: Session = Depends(get_db)):
    calculation = db.query(models.Calculation).filter(models.Calculation.id == calculation_id).first()
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")

    db.delete(calculation)
    db.commit()
    return None
