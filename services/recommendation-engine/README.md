# Recommendation Engine

ML-powered travel destination recommendation service.

## Overview
This service uses a trained Random Forest model to recommend travel destinations based on user preferences and budget.

## API Endpoints

### Health Check
```bash
GET /health
```

### Get Recommendation
```bash
POST /recommend
Content-Type: application/json

{
  "age": 30,
  "budget": 3000,
  "travel_days": 7,
  "preferred_activity": "Beach",
  "travel_month": 6,
  "group_size": 2
}
```

Response:
```json
{
  "destination": "Bali",
  "confidence": 0.92,
  "explanation": "Great beach destination for budget-conscious travelers"
}
```

## Development

### Local Development
```bash
cd services/recommendation-engine
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### Testing
```bash
pytest tests/ -v
```

## Environment Variables
- `MODEL_PATH`: Path to trained model (default: `/app/models/recommendation_model.pkl`)
- `DATABASE_URL`: PostgreSQL connection string (optional)

## Docker Build
```bash
docker build -t recommendation-engine:latest .
docker run -p 8001:8000 recommendation-engine:latest
```

## Performance
- Inference time: < 100ms
- Model accuracy: > 85%
- Throughput: 1000+ requests/second (with caching)
