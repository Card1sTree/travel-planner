import pandas as pd

def prepare_data():
    """Prepare and preprocess data"""
    print("📦 Preparing data...")
    
    # Simulated data preparation
    destinations = ['Paris', 'Tokyo', 'New York', 'Bali', 'Sydney', 'Dubai', 'Rome', 'Barcelona']
    activities = ['Beach', 'Culture', 'Adventure', 'Nightlife', 'Food', 'Nature']
    
    import numpy as np
    np.random.seed(42)
    
    data = {
        'age': np.random.randint(18, 80, 1000),
        'budget': np.random.randint(500, 10000, 1000),
        'travel_days': np.random.randint(3, 30, 1000),
        'preferred_activity': np.random.choice(activities, 1000),
        'travel_month': np.random.randint(1, 12, 1000),
        'group_size': np.random.randint(1, 10, 1000),
        'destination': np.random.choice(destinations, 1000)
    }
    
    df = pd.DataFrame(data)
    
    # Save processed data
    df.to_csv('data/processed_travel_data.csv', index=False)
    print(f"✅ Data prepared: {len(df)} samples processed")

if __name__ == '__main__':
    prepare_data()
