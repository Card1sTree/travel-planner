from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Trip Planner", version="1.0.0")

RECOMMENDATION_ENGINE_URL = os.getenv('RECOMMENDATION_ENGINE_URL', 'http://localhost:8001')

# In-memory storage for demo
trips_db = {}

class TripRequest(BaseModel):
    user_id: str
    start_date: str
    end_date: str
    budget: float
    preferred_activity: str

class ItineraryItem(BaseModel):
    day: int
    activity: str
    location: str
    estimated_cost: float

class TripPlan(BaseModel):
    trip_id: str
    user_id: str
    destination: str
    start_date: str
    end_date: str
    total_budget: float
    total_cost: float
    itinerary: list[ItineraryItem]
    created_at: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "trip-planner"}

@app.post("/trips", response_model=TripPlan)
async def create_trip(request: TripRequest):
    """Create a trip plan with recommended destination"""
    try:
        # Get recommendation from recommendation engine
        logger.info(f"📍 Requesting recommendation for user {request.user_id}")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{RECOMMENDATION_ENGINE_URL}/recommend",
                    json={
                        "age": 30,  # Demo data
                        "budget": request.budget,
                        "travel_days": 7,
                        "preferred_activity": request.preferred_activity,
                        "travel_month": 6,
                        "group_size": 1
                    },
                    timeout=10.0
                )
                recommendation = response.json()
                destination = recommendation.get('destination', 'Paris')
            except Exception as e:
                logger.warning(f"⚠️ Could not reach recommendation engine, using default: {e}")
                destination = "Paris"
        
        # Generate itinerary
        start = datetime.fromisoformat(request.start_date)
        end = datetime.fromisoformat(request.end_date)
        num_days = (end - start).days
        
        itinerary = []
        activities = ['Sightseeing', 'Museum Visit', 'Local Food Tour', 'Shopping', 'Adventure Activity']
        daily_cost = request.budget / max(num_days, 1)
        
        for day in range(1, num_days + 1):
            itinerary.append(ItineraryItem(
                day=day,
                activity=activities[day % len(activities)],
                location=destination,
                estimated_cost=daily_cost
            ))
        
        # Create trip
        trip_id = f"trip_{len(trips_db) + 1}"
        total_cost = sum(item.estimated_cost for item in itinerary)
        
        trip = {
            "trip_id": trip_id,
            "user_id": request.user_id,
            "destination": destination,
            "start_date": request.start_date,
            "end_date": request.end_date,
            "total_budget": request.budget,
            "total_cost": total_cost,
            "itinerary": itinerary,
            "created_at": datetime.now().isoformat()
        }
        
        trips_db[trip_id] = trip
        logger.info(f"✅ Trip created: {trip_id} to {destination}")
        
        return TripPlan(**trip)
    
    except Exception as e:
        logger.error(f"❌ Error creating trip: {e}")
        raise HTTPException(status_code=400, detail="Error creating trip plan")

@app.get("/trips/{trip_id}", response_model=TripPlan)
def get_trip(trip_id: str):
    """Get trip details"""
    if trip_id not in trips_db:
        logger.warning(f"⚠️ Trip not found: {trip_id}")
        raise HTTPException(status_code=404, detail="Trip not found")
    
    return TripPlan(**trips_db[trip_id])

@app.get("/users/{user_id}/trips")
def get_user_trips(user_id: str):
    """Get all trips for a user"""
    user_trips = [trip for trip in trips_db.values() if trip['user_id'] == user_id]
    logger.info(f"📋 Retrieved {len(user_trips)} trips for user {user_id}")
    return {"user_id": user_id, "trips": user_trips}

@app.get("/")
def root():
    return {
        "service": "Travel Trip Planner",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "create_trip": "POST /trips",
            "get_trip": "GET /trips/{trip_id}",
            "user_trips": "GET /users/{user_id}/trips",
            "docs": "/docs"
        }
    }
