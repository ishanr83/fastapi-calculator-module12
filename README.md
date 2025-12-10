# FastAPI Calculator - Module 12

A production-ready FastAPI application with PostgreSQL database, user authentication, and calculation management.

## Features

- User registration and authentication
- BREAD operations for calculations (Browse, Read, Edit, Add, Delete)
- PostgreSQL database with SQLAlchemy ORM
- Comprehensive test suite with 90%+ coverage
- Docker containerization
- CI/CD with GitHub Actions
- Automatic Docker Hub deployment

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Run the Application
```bash
# Clone the repository
git clone https://github.com/ishanr83/fastapi-calculator-module12.git
cd fastapi-calculator-module12

# Start all services
docker-compose up --build -d

# Access the application
# API: http://localhost:8000
# Swagger Docs: http://localhost:8000/docs
# pgAdmin: http://localhost:5050
```

## Running Tests

### Local Testing with Docker

1. Start all services:
```bash
   docker-compose up --build -d
```

2. Run tests inside the container:
```bash
   docker-compose exec fastapi pytest --maxfail=1 --disable-warnings --cov=app --cov-report=term-missing
```

3. View test coverage results in the output (90%+ coverage).

### Manual API Testing

1. Open Swagger UI: http://localhost:8000/docs

2. Test the following workflow:
   - Register a user (POST /users/register)
   - Login with that user (POST /users/login)
   - Create a calculation (POST /calculations) - use user_id from registration
   - List all calculations (GET /calculations)
   - Update a calculation (PUT /calculations/{id})
   - Delete a calculation (DELETE /calculations/{id})

## Project Structure
```
fastapi-calculator-module12/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app with all endpoints
│   ├── operations.py     # Calculator operations
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── auth.py           # Password hashing utilities
│   └── database.py       # Database configuration
├── tests/
│   ├── test_calculations.py  # Calculation endpoint tests
│   ├── test_users.py         # User endpoint tests
│   ├── test_api_endpoints.py # API endpoint tests
│   └── test_operations.py    # Operation function tests
├── .github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions CI/CD
├── docker-compose.yml    # Multi-container setup
├── Dockerfile            # FastAPI container
└── requirements.txt      # Python dependencies
```

## Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **PostgreSQL**: Relational database
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation using Python type hints
- **Pytest**: Testing framework with 90%+ coverage
- **Docker**: Containerization
- **GitHub Actions**: CI/CD pipeline
- **pgAdmin**: Database management tool

## CI/CD Pipeline

Every push to `main` triggers:
1. PostgreSQL service starts
2. Dependencies install
3. All tests run with coverage report (90%+)
4. Docker image builds
5. Image pushes to Docker Hub (on success)

View workflow: https://github.com/ishanr83/fastapi-calculator-module12/actions

## Docker Hub

Docker image: https://hub.docker.com/r/ishanr83/fastapi-calculator-module12

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Calculator UI
- `GET /` - Interactive calculator interface

### Calculator API
- `GET /api/add?a={a}&b={b}` - Add two numbers
- `GET /api/subtract?a={a}&b={b}` - Subtract two numbers
- `GET /api/multiply?a={a}&b={b}` - Multiply two numbers
- `GET /api/divide?a={a}&b={b}` - Divide two numbers

### User Management
- `POST /users/register` - Register a new user
- `POST /users/login` - Login and verify credentials

### Calculations (BREAD)
- `GET /calculations` - Browse all calculations
- `GET /calculations/{id}` - Read a specific calculation
- `POST /calculations` - Add a new calculation
- `PUT /calculations/{id}` - Edit an existing calculation
- `DELETE /calculations/{id}` - Delete a calculation

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (default: `postgresql://postgres:postgres@db:5432/fastapi_db`)

## Development
```bash
# Install dependencies locally (optional)
pip install -r requirements.txt

# Run tests locally (requires PostgreSQL)
pytest --cov=app

# Stop all services
docker-compose down

# Remove all data
docker-compose down -v
```

## License

MIT

## Author

Ishan Ranade
