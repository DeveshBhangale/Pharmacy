import tensorflow as tf
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime, UTC

from app.core.config import settings
from app.models.pharmacy import Medicine, Prescription, PrescriptionItem

def load_data():
    # Create database connection
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Load medicines
        medicines = pd.read_sql(db.query(Medicine).statement, db.bind)
        
        # Load prescriptions and items
        prescriptions = pd.read_sql(db.query(Prescription).statement, db.bind)
        prescription_items = pd.read_sql(db.query(PrescriptionItem).statement, db.bind)
        
        return medicines, prescriptions, prescription_items
    finally:
        db.close()

def preprocess_data(medicines, prescriptions, prescription_items):
    # Create medicine embeddings
    medicine_categories = pd.get_dummies(medicines['category'])
    medicine_embeddings = pd.concat([
        medicines[['id', 'price']],
        medicine_categories
    ], axis=1)
    
    # Create user-medicine interaction matrix
    user_medicines = prescription_items.merge(
        prescriptions[['id', 'user_id']],
        left_on='prescription_id',
        right_on='id'
    )
    
    # Create features for each user
    user_features = []
    for user_id in user_medicines['user_id'].unique():
        user_prescriptions = user_medicines[user_medicines['user_id'] == user_id]
        
        # Get user's medicine history
        user_medicine_ids = user_prescriptions['medicine_id'].unique()
        user_medicine_embeddings = medicine_embeddings[
            medicine_embeddings['id'].isin(user_medicine_ids)
        ]
        
        # Calculate average features
        avg_features = user_medicine_embeddings.mean()
        user_features.append({
            'user_id': user_id,
            'features': avg_features.values
        })
    
    return np.array([uf['features'] for uf in user_features])

def create_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=input_shape),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(16, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model():
    print("Loading data...")
    medicines, prescriptions, prescription_items = load_data()
    
    print("Preprocessing data...")
    X = preprocess_data(medicines, prescriptions, prescription_items)
    
    print("Creating and training model...")
    model = create_model((X.shape[1],))
    
    # Create dummy labels for demonstration
    y = np.random.randint(0, 16, size=(X.shape[0],))
    y = tf.keras.utils.to_categorical(y, num_classes=16)
    
    # Train the model
    model.fit(
        X, y,
        epochs=10,
        batch_size=32,
        validation_split=0.2
    )
    
    # Create models directory if it doesn't exist
    os.makedirs(settings.MODEL_PATH, exist_ok=True)
    
    # Save the model
    model_path = os.path.join(settings.MODEL_PATH, "medicine_recommender.h5")
    model.save(model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model() 