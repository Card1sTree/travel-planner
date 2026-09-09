from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="User API", version="1.0.0")

# In-memory storage for demo (replace with DB)
users_db = {}

class UserProfile(BaseModel):
    name: str
    email: str
    age: int
    budget: float
    preferred_activities: list[str]

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = None
    budget: float | None = None
    preferred_activities: list[str] | None = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    age: int
    budget: float
    preferred_activities: list[str]
    created_at: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "user-api"}

@app.post("/users", response_model=UserResponse)
def create_user(user: UserProfile):
    """Create a new user profile"""
    try:
        user_id = f"user_{len(users_db) + 1}"
        users_db[user_id] = {
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "budget": user.budget,
            "preferred_activities": user.preferred_activities,
            "created_at": datetime.now().isoformat()
        }
        logger.info(f"✅ User created: {user_id}")
        return UserResponse(id=user_id, **users_db[user_id])
    except Exception as e:
        logger.error(f"❌ Error creating user: {e}")
        raise HTTPException(status_code=400, detail="Error creating user")

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    """Get user profile by ID"""
    if user_id not in users_db:
        logger.warning(f"⚠️ User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(id=user_id, **users_db[user_id])

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user: UserUpdate):
    """Update user profile"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        user_data = users_db[user_id]
        if user.name:
            user_data['name'] = user.name
        if user.email:
            user_data['email'] = user.email
        if user.age:
            user_data['age'] = user.age
        if user.budget:
            user_data['budget'] = user.budget
        if user.preferred_activities:
            user_data['preferred_activities'] = user.preferred_activities
        
        logger.info(f"✅ User updated: {user_id}")
        return UserResponse(id=user_id, **user_data)
    except Exception as e:
        logger.error(f"❌ Error updating user: {e}")
        raise HTTPException(status_code=400, detail="Error updating user")

@app.get("/")
def root():
    return {
        "service": "Travel Planner User API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "create_user": "POST /users",
            "get_user": "GET /users/{user_id}",
            "update_user": "PUT /users/{user_id}",
            "docs": "/docs"
        }
    }
