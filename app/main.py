"""FastAPI Calculator Application."""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import app.operations as op

app = FastAPI(title="FastAPI Calculator - Module 9")


@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serve the calculator UI."""
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI Calculator - Module 9</title>
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
        <p style="text-align: center; color: #666;">Module 9: Docker + PostgreSQL</p>
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
    """Execute calculation with error handling."""
    try:
        return func(a, b)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/add")
def add(a: float, b: float):
    """Add two numbers."""
    return {"operation": "add", "result": _calc(op.add, a, b)}


@app.get("/api/subtract")
def subtract(a: float, b: float):
    """Subtract b from a."""
    return {"operation": "subtract", "result": _calc(op.subtract, a, b)}


@app.get("/api/multiply")
def multiply(a: float, b: float):
    """Multiply two numbers."""
    return {"operation": "multiply", "result": _calc(op.multiply, a, b)}


@app.get("/api/divide")
def divide(a: float, b: float):
    """Divide a by b."""
    return {"operation": "divide", "result": _calc(op.divide, a, b)}
