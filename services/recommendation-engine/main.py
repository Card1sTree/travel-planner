from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Recommendation Engine", version="1.0.0")

# Load model at startup
model = None
scaler = None
activity_encoder = None

@app.on_event("startup")
def load_model():
    global model, scaler, activity_encoder
    model_path = os.getenv('MODEL_PATH', '/app/models/recommendation_model.pkl')
    scaler_path = os.getenv('MODEL_PATH', '/app/models/scaler.pkl').replace('recommendation_model.pkl', 'scaler.pkl')
    encoder_path = os.getenv('MODEL_PATH', '/app/models/activity_encoder.pkl').replace('recommendation_model.pkl', 'activity_encoder.pkl')
    
    try:
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            activity_encoder = joblib.load(encoder_path)
            logger.info("✅ Model loaded successfully")
        else:
            logger.warning(f"⚠️ Model not found at {model_path}, using demo mode")
    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")

class TravelPreferences(BaseModel):
    age: int
    budget: float
    travel_days: int
    preferred_activity: str
    travel_month: int
    group_size: int

class RecommendationResponse(BaseModel):
    destination: str
    confidence: float
    explanation: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "recommendation-engine"}

@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendation(preferences: TravelPreferences):
    """Get destination recommendation based on user preferences"""
    if model is None:
        # Demo response if model not loaded
        logger.warning("Model not available, returning demo recommendation")
        return RecommendationResponse(
            destination="Paris",
            confidence=0.85,
            explanation="Based on your preferences for culture and moderate budget, Paris is perfect!"
        )
    
    try:
        # Encode activity
        activity_encoded = activity_encoder.transform([preferences.preferred_activity])[0]
        
        # Prepare features
        features = np.array([[
            preferences.age,
            preferences.budget,
            preferences.travel_days,
            activity_encoded,
            preferences.travel_month,
            preferences.group_size
        ]])
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        confidence = float(model.predict_proba(features_scaled).max())
        
        explanations = {
            'Paris': 'Perfect for culture enthusiasts with moderate to high budget',
            'Tokyo': 'Ideal for adventure seekers and tech lovers',
            'Bali': 'Great beach destination for budget-conscious travelers',
            'Sydney': 'Best for outdoor adventures and beach lovers',
            'Dubai': 'Luxury destination for high-budget travelers',
            'New York': 'Perfect for nightlife and urban exploration',
            'Rome': 'Excellent for history and culture buffs',
            'Barcelona': 'Great balance of beach, culture, and nightlife'
        }
        
        explanation = explanations.get(prediction, "A wonderful destination awaits!")
        
        logger.info(f"✅ Recommendation generated: {prediction} with confidence {confidence:.2f}")
        
        return RecommendationResponse(
            destination=prediction,
            confidence=confidence,
            explanation=explanation
        )
    
    except Exception as e:
        logger.error(f"❌ Error generating recommendation: {e}")
        raise HTTPException(status_code=500, detail="Error generating recommendation")

@app.get("/")
def root():
    return {
        "service": "Travel Recommendation Engine",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "recommend": "/recommend",
            "docs": "/docs"
        }
    }
