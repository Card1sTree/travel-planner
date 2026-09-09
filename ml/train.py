import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import json
from datetime import datetime

# Sample training data for travel recommendations
def generate_sample_data():
    """Generate sample travel data for training"""
    np.random.seed(42)
    
    destinations = ['Paris', 'Tokyo', 'New York', 'Bali', 'Sydney', 'Dubai', 'Rome', 'Barcelona']
    activities = ['Beach', 'Culture', 'Adventure', 'Nightlife', 'Food', 'Nature']
    
    data = {
        'age': np.random.randint(18, 80, 1000),
        'budget': np.random.randint(500, 10000, 1000),
        'travel_days': np.random.randint(3, 30, 1000),
        'preferred_activity': np.random.choice(activities, 1000),
        'travel_month': np.random.randint(1, 12, 1000),
        'group_size': np.random.randint(1, 10, 1000),
        'destination': np.random.choice(destinations, 1000)
    }
    
    return pd.DataFrame(data)

def train_recommendation_model():
    """Train recommendation model"""
    print("🔄 Loading training data...")
    df = generate_sample_data()
    
    # Prepare features
    print("🔄 Preparing features...")
    X = df.drop('destination', axis=1)
    y = df['destination']
    
    # Encode categorical variables
    le_activity = LabelEncoder()
    X['preferred_activity'] = le_activity.fit_transform(X['preferred_activity'])
    
    # Scale numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train model
    print("🔄 Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_scaled, y)
    
    # Save model and encoders
    print("💾 Saving model and artifacts...")
    joblib.dump(model, 'ml/models/recommendation_model.pkl')
    joblib.dump(scaler, 'ml/models/scaler.pkl')
    joblib.dump(le_activity, 'ml/models/activity_encoder.pkl')
    
    # Calculate metrics
    train_score = model.score(X_scaled, y)
    metrics = {
        'accuracy': float(train_score),
        'n_samples': len(df),
        'n_features': X_scaled.shape[1],
        'timestamp': datetime.now().isoformat()
    }
    
    print(f"✅ Model trained with accuracy: {train_score:.4f}")
    
    # Save metrics
    with open('metrics.json', 'w') as f:
        json.dump(metrics, f)
    
    return model, metrics

if __name__ == '__main__':
    train_recommendation_model()
    print("✅ Training complete!")
