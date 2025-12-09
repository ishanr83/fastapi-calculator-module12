# Module 9: FastAPI Calculator with Docker and PostgreSQL

## Project Overview
This project demonstrates:
- Docker containerization with Docker Compose
- FastAPI web application
- PostgreSQL database integration
- Database relationships (one-to-many with foreign keys)
- Complete CRUD operations via SQL

## Architecture
- FastAPI: Web framework serving calculator API and UI
- PostgreSQL: Relational database storing users and calculations
- pgAdmin: Web-based database management interface
- Docker Compose: Orchestrates all services

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git installed

### Setup and Run

1. Clone the repository:

   git clone https://github.com/YOUR_USERNAME/fastapi-calculator-module9.git
   cd fastapi-calculator-module9

2. Start all services:

   docker-compose up --build -d

3. Access the applications:
   - FastAPI Calculator: http://localhost:8000
   - pgAdmin: http://localhost:5050
     - Email: admin@admin.com
     - Password: admin

4. Stop services:

   docker-compose down

## Database Setup

### Connect pgAdmin to PostgreSQL

1. Open pgAdmin at:  
   http://localhost:5050

2. Login with credentials above

3. Right-click "Servers" → "Register" → "Server"

4. General tab:
   - Name: FastAPI DB

5. Connection tab:
   - Host: db
   - Port: 5432
   - Database: fastapi_db
   - Username: postgres
   - Password: postgres
   - Save password: checked

6. Click "Save"

### Run SQL Operations

1. Open Query Tool:  
   Right-click "fastapi_db" → "Query Tool"

2. Open file:
   sql_scripts/module9_operations.sql

3. Run each section separately

4. Take screenshots for documentation

## Database Schema

### Users Table

users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

### Calculations Table

calculations (
    id SERIAL PRIMARY KEY,
    operation VARCHAR(20) NOT NULL,
    operand_a FLOAT NOT NULL,
    operand_b FLOAT NOT NULL,
    result FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
)

Relationship: One user can have many calculations (one-to-many)

## Required Screenshots

1. CREATE TABLES - Table creation success  
2. INSERT RECORDS - Insert success messages  
3. SELECT USERS - All users displayed  
4. SELECT CALCULATIONS - All calculations displayed  
5. JOIN QUERY - Joined data with usernames  
6. UPDATE RECORD - Updated result value  
7. DELETE RECORD - Fewer records after deletion  
8. DOCKER STATUS - All containers running (output of: docker-compose ps)

## Learning Outcomes

- Applied containerization with Docker Compose
- Integrated Python FastAPI with PostgreSQL
- Demonstrated one-to-many relationships with foreign keys
- Performed complete CRUD operations in SQL

## Technologies Used

- Python 3.12
- FastAPI 0.104.1
- PostgreSQL 15
- pgAdmin 4
- Docker and Docker Compose
- SQLAlchemy 2.0

## Project Structure

fastapi-calculator-module9  
├── app  
│   ├── __init__.py  
│   ├── main.py  
│   └── operations.py  
├── sql_scripts  
│   └── module9_operations.sql  
├── tests  
│   └── __init__.py  
├── docker-compose.yml  
├── Dockerfile  
├── requirements.txt  
├── .gitignore  
└── README.md  

## Troubleshooting

### Ports Already in Use

- Stop current containers:

  docker-compose down

- Restart:

  docker-compose up -d

If needed, edit "docker-compose.yml" and change ports for:
- FastAPI (8000)
- PostgreSQL (5432)
- pgAdmin (5050)

### Cannot Connect to Database

- Verify host is "db" (not "localhost") in pgAdmin
- Check containers:

  docker-compose ps

- View database logs:

  docker-compose logs db

### Reset Everything

- Remove containers and volumes:

  docker-compose down -v

- Rebuild and start:

  docker-compose up --build -d

## Author

Your Name - IS 218 Module 9 Assignment

## Date

November 2024

## Repository

https://github.com/YOUR_USERNAME/fastapi-calculator-module9
