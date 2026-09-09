# User API

User profile and preference management service.

## Overview
REST API for managing user profiles, preferences, and travel history.

## API Endpoints

### Health Check
```bash
GET /health
```

### Create User
```bash
POST /users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "budget": 3000.0,
  "preferred_activities": ["Beach", "Culture", "Food"]
}
```

### Get User
```bash
GET /users/{user_id}
```

### Update User
```bash
PUT /users/{user_id}
Content-Type: application/json

{
  "name": "Jane Doe",
  "budget": 5000.0
}
```

## Development

### Local Development
```bash
cd services/user-api
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

## Database
Uses PostgreSQL. Connection via `DATABASE_URL` environment variable.

## Authentication
Currently no authentication (add JWT/OAuth for production).

## Scalability
- Horizontal scaling: Increase replicas in Kubernetes
- Database: Migrate to managed service (AWS RDS, Cloud SQL)
- Caching: Add Redis for frequently accessed profiles
