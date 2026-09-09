# Trip Planner

Itinerary planning and trip coordination service.

## Overview
Orchestrates trip planning by:
1. Calling Recommendation Engine for destination suggestions
2. Building detailed itineraries
3. Calculating trip costs

## API Endpoints

### Health Check
```bash
GET /health
```

### Create Trip Plan
```bash
POST /trips
Content-Type: application/json

{
  "user_id": "user_1",
  "start_date": "2024-06-01",
  "end_date": "2024-06-08",
  "budget": 3000.0,
  "preferred_activity": "Beach"
}
```

Response includes:
- Recommended destination
- Day-by-day itinerary
- Cost breakdown
- Total estimated cost

### Get Trip Details
```bash
GET /trips/{trip_id}
```

### Get User's Trips
```bash
GET /users/{user_id}/trips
```

## Development

### Local Development
```bash
cd services/trip-planner
pip install -r requirements.txt
RECOMMENDATION_ENGINE_URL=http://localhost:8001 \
uvicorn main:app --reload --port 8003
```

## Service Mesh Integration
Ready for Istio/Linkerd for:
- Service-to-service communication
- Load balancing
- Circuit breaking
- Retry policies

## Monitoring
Exposes Prometheus metrics (can be added):
- Trip creation latency
- Recommendation engine response time
- Error rates
