# 🚀 Space Mission Control API

A fun and comprehensive demonstration of **Pydantic** data validation and **FastAPI** routing through a space mission control system simulation.

## 📋 Overview

This project showcases how to build a robust REST API using FastAPI and Pydantic. The system simulates a space mission control center where you can:

- **Register astronauts** with validated credentials and experience
- **Create space missions** with specific requirements and constraints
- **Assign crew members** to missions with role-based validation
- **Track mission status** and crew assignments

## ✨ Features

### Pydantic Validation Demonstrations

The project showcases various Pydantic features:

- **Field Constraints**: Min/max values, string length, pattern matching
- **Email Validation**: Using `EmailStr` for proper email format
- **Custom Validators**: Business logic validation (e.g., experience vs. age)
- **Literal Types**: Restricted choices for fields (status, specialization, roles)
- **Cross-field Validation**: Validating relationships between fields
- **DateTime Handling**: Future date validation for launch dates
- **Optional Fields**: Default values and nullable fields

### FastAPI Features

- **RESTful API Design**: Proper HTTP methods and status codes
- **Auto-generated Documentation**: Interactive Swagger UI and ReDoc
- **Type Safety**: Full type hints and validation
- **Error Handling**: Comprehensive HTTP exceptions
- **Query Parameters**: Filtering and search capabilities
- **Response Models**: Structured API responses

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Navigate to the project directory**:
```bash
cd C:\Users\Usuario\github\ai-engineering-patterns\05-fastapi-pydantic
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

## 📚 API Documentation

### Astronaut Endpoints

#### Create Astronaut
```http
POST /astronauts/
```

**Request Body**:
```json
{
  "name": "Sarah Connor",
  "age": 35,
  "email": "sarah.connor@nasa.space",
  "specialization": "pilot",
  "years_of_experience": 12,
  "active": true
}
```

**Validation Rules**:
- Name: 2-100 characters, no numbers
- Age: 21-65 years
- Email: Valid email format
- Specialization: One of `pilot`, `engineer`, `scientist`, `medic`, `commander`
- Experience: 0-40 years, cannot exceed (age - 18)

#### List Astronauts
```http
GET /astronauts/?active_only=true&specialization=pilot
```

#### Get Specific Astronaut
```http
GET /astronauts/{astronaut_id}
```

#### Update Astronaut
```http
PUT /astronauts/{astronaut_id}
```

#### Delete Astronaut
```http
DELETE /astronauts/{astronaut_id}
```

---

### Mission Endpoints

#### Create Mission
```http
POST /missions/
```

**Request Body**:
```json
{
  "name": "Mars Odyssey",
  "destination": "Mars",
  "duration_days": 180,
  "status": "planning",
  "launch_date": "2025-06-15T10:00:00",
  "crew_capacity": 6
}
```

**Validation Rules**:
- Name: 3-100 characters, auto-capitalized
- Duration: 1-1000 days
- Status: One of `planning`, `active`, `completed`, `cancelled`
- Launch Date: Must be in the future
- Crew Capacity: 1-10 members
- Current Crew Count: Cannot exceed capacity

#### List Missions
```http
GET /missions/?status=planning
```

#### Get Specific Mission
```http
GET /missions/{mission_id}
```

#### Update Mission
```http
PUT /missions/{mission_id}
```

---

### Crew Assignment Endpoints

#### Assign Astronaut to Mission
```http
POST /missions/{mission_id}/assign
```

**Request Body**:
```json
{
  "astronaut_id": 1,
  "mission_id": 1,
  "role": "commander"
}
```

**Validation Rules**:
- Astronaut must exist and be active
- Mission must exist and have available capacity
- Astronaut cannot be assigned to the same mission twice
- Role: One of `commander`, `pilot`, `engineer`, `scientist`, `medic`, `specialist`

#### Get Mission Crew
```http
GET /missions/{mission_id}/crew
```

#### Get Astronaut's Missions
```http
GET /astronauts/{astronaut_id}/missions
```

---

### System Endpoints

#### Health Check
```http
GET /health
```

Returns system statistics and status.

## 🎯 Usage Examples

### Example 1: Register an Astronaut

```bash
curl -X POST "http://localhost:8000/astronauts/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Neil Armstrong",
    "age": 38,
    "email": "neil.armstrong@nasa.space",
    "specialization": "commander",
    "years_of_experience": 15
  }'
```

### Example 2: Create a Mission

```bash
curl -X POST "http://localhost:8000/missions/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Apollo 11",
    "destination": "Moon",
    "duration_days": 8,
    "crew_capacity": 3,
    "launch_date": "2025-07-16T13:32:00"
  }'
```

### Example 3: Assign Crew to Mission

```bash
curl -X POST "http://localhost:8000/missions/1/assign" \
  -H "Content-Type: application/json" \
  -d '{
    "astronaut_id": 1,
    "mission_id": 1,
    "role": "commander"
  }'
```

## 🧪 Testing Pydantic Validation

Try these examples to see Pydantic validation in action:

### Invalid Age (Too Young)
```json
{
  "name": "John Doe",
  "age": 18,
  "email": "john@nasa.space",
  "specialization": "pilot",
  "years_of_experience": 5
}
```
**Error**: Age must be between 21 and 65

### Invalid Experience
```json
{
  "name": "Jane Smith",
  "age": 30,
  "email": "jane@nasa.space",
  "specialization": "engineer",
  "years_of_experience": 20
}
```
**Error**: Experience years (20) cannot exceed age minus 18 (12)

### Invalid Email
```json
{
  "name": "Bob Wilson",
  "age": 35,
  "email": "not-an-email",
  "specialization": "scientist",
  "years_of_experience": 10
}
```
**Error**: Invalid email format

### Name with Numbers
```json
{
  "name": "Agent007",
  "age": 35,
  "email": "agent@nasa.space",
  "specialization": "pilot",
  "years_of_experience": 10
}
```
**Error**: Name cannot contain numbers

## 📁 Project Structure

```
05-fastapi-pydantic/
├── main.py              # FastAPI application with all endpoints
├── models.py            # Pydantic models with validation
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## 🔍 Key Learning Points

### Pydantic Features Demonstrated

1. **Field Validation**: Using `Field()` with constraints
2. **Custom Validators**: `@field_validator` decorator for complex logic
3. **Type Hints**: Leveraging Python's type system
4. **Email Validation**: Built-in `EmailStr` type
5. **Literal Types**: Restricting values to specific choices
6. **Model Configuration**: Using `Config` class for examples
7. **Cross-field Validation**: Accessing other field values in validators

### FastAPI Features Demonstrated

1. **Path Operations**: GET, POST, PUT, DELETE
2. **Request Validation**: Automatic validation via Pydantic
3. **Response Models**: Type-safe responses
4. **Status Codes**: Proper HTTP status code usage
5. **Error Handling**: HTTPException for errors
6. **Query Parameters**: Filtering and search
7. **Path Parameters**: Resource identification
8. **Auto Documentation**: Swagger UI and ReDoc
9. **Tags**: Organizing endpoints in documentation

## 🎓 Educational Value

This project is perfect for learning:

- How Pydantic validates data automatically
- How to create custom validation logic
- RESTful API design principles
- FastAPI routing and dependency injection
- Error handling in web APIs
- API documentation best practices

## 🚧 Future Enhancements

This is a demonstration project. In a production environment, consider:

- **Database Integration**: Replace in-memory storage with PostgreSQL/MongoDB
- **Authentication**: Add JWT-based authentication
- **Testing**: Add unit and integration tests
- **Logging**: Implement structured logging
- **CORS**: Configure CORS for frontend integration
- **Pagination**: Add pagination for list endpoints
- **Caching**: Implement Redis caching
- **Docker**: Containerize the application

## 📝 License

This is a demonstration project for educational purposes.

## 🤝 Contributing

Feel free to extend this project with additional features or improvements!

---

**Happy Coding! 🚀**
